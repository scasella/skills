---
name: modal-gpu
description: >
  Run short, bounded commands on remote Modal GPU sandboxes from Codex when
  local hardware has no CUDA/GPU. Use for CUDA sanity checks, GPU-path tests,
  training smoke tests, and short benchmarks. Prefer Modal Functions/jobs for
  training, fine-tuning, sweeps, and batch experiments. Triggers on: "run on
  GPU", "test on CUDA", "Modal sandbox", "GPU benchmark", or GPU validation.
---

# Modal GPU Short-Run Sandbox Runner

Use this skill when an implementation must be validated on real GPU hardware and
local execution is CPU-only. This is not the default training environment:
multi-hour training, fine-tuning, sweeps, and batch evals should be wrapped as
bounded Modal Functions with Volumes/checkpoints.

## Cost-First Scope

- Use CPU/local tests before remote GPU.
- Use T4 or L4 for CUDA sanity checks and cheap integration smoke tests.
- Use A10 or L4 for small representative training smoke tests.
- Use L40S for around 48 GB VRAM and A100 80GB for true 80 GB needs.
- Use H100/H200/B200 only with benchmark evidence or explicit user direction.
- Keep Codex Cloud attempts at `1` for tasks that can launch Modal jobs.

Before any GPU launch, print GPU, CPU, memory, timeout, estimated max cost,
app/run name, and cleanup command. If expected runtime is more than a short
smoke, switch to `modal-gpu-experiment`.

## Codex Workflow

1. Decide primitive: Function for training/jobs, Sandbox only for short stateful
   GPU validation or debugging.
2. Verify Modal install + auth.
3. Ensure a repo-local runner exists (`scripts/modal_gpu.py`).
4. Run a cheap CUDA sanity check first on T4/L4/A10.
5. Run the target command with explicit GPU, CPU, memory, and timeout.
6. Report evidence (command, GPU, runtime, exit code, key metrics) and verify cleanup.

## Prerequisites

Before running any Modal command, verify:

1. `modal` import works in host Python (not a project venv unless intentional):
   ```bash
   python3 -c "import modal; print(modal.__version__)"
   ```
   If missing:
   ```bash
   pip install modal
   ```

2. Modal auth is configured:
   ```bash
   modal profile list
   ```
   If not configured:
   ```bash
   modal setup
   ```

3. You are at project root.

## Runner Contract (`scripts/modal_gpu.py`)

Expected invocation:

```bash
python scripts/modal_gpu.py [OPTIONS] -- COMMAND...
```

Options:
- `--gpu GPU`: `T4` or `L4` for smoke, `A10`/`A10G` for small training smoke,
  `L40S` or `A100-80GB` only when VRAM requires it
- `--timeout MINS`: sandbox timeout in minutes (default `30`, hard cap `120`)
- new/updated runners should also expose explicit `--cpu`, `--memory`, and
  `--idle-timeout` with idle timeout capped at 300 seconds

`--` is required between runner options and the target command.

## Modal API Notes (v1.3+)

Use this pattern:

```python
import modal
import time
from datetime import datetime, timezone, timedelta

MAX_SECONDS = 30 * 60


def utc_expiry(seconds: int) -> str:
    return (datetime.now(timezone.utc) + timedelta(seconds=seconds)).isoformat()

image = (
    modal.Image.debian_slim(python_version="3.10")
    .pip_install("torch==2.9.1", extra_index_url="https://download.pytorch.org/whl/cu128")
    .pip_install("other-dep>=1.0")
    .add_local_dir(repo_root, remote_path="/app")
)

app = modal.App.lookup("my-sandbox", create_if_missing=True)

sandbox = modal.Sandbox.create(
    *command,
    image=image,
    gpu="T4",
    cpu=1,
    memory=4096,
    timeout=MAX_SECONDS,
    idle_timeout=300,
    name=f"codex-gpu-smoke-{int(time.time())}",
    workdir="/app",
    app=app,
)

sandbox.set_tags({
    "owner": "codex",
    "purpose": "gpu-smoke",
    "expires_at": utc_expiry(MAX_SECONDS),
})

try:
    for line in sandbox.stdout:
        print(line, end="")

    sandbox.wait(raise_on_termination=False)
    exit_code = sandbox.returncode
finally:
    sandbox.terminate()
```

Important details:
- Do not use deprecated `modal.Mount` / `Mount.from_local_dir()`.
- `Sandbox.create` does not take `mounts`; use `Image.add_local_dir()`.
- `sandbox.wait()` returns `None`; read `sandbox.returncode`.
- Use `raise_on_termination=False` so non-zero exits propagate cleanly.
- All Sandbox creation paths must include explicit `timeout`, `idle_timeout`,
  `cpu`, `memory`, `name`, tags, and a `finally: terminate()` cleanup path.

## Common Commands

CUDA sanity check:

```bash
python scripts/modal_gpu.py -- python -c "import torch; print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0))"
```

Run GPU tests:

```bash
python scripts/modal_gpu.py -- python -m pytest tests/ -x -v
```

Single test file:

```bash
python scripts/modal_gpu.py -- python -m pytest tests/test_gpt.py -x -v
```

Tiny training smoke test only. For real training, write a Modal Function with
Volumes and checkpoints via `modal-gpu-experiment`:

```bash
python scripts/modal_gpu.py -- python -m scripts.base_train \
  --depth=4 --max-seq-len=512 --device-batch-size=4 \
  --total-batch-size=2048 --eval-tokens=2048 \
  --core-metric-every=-1 --sample-every=-1 --num-iterations=5
```

Multi-step command:

```bash
python scripts/modal_gpu.py -- bash -lc "python -m project.dataset -n 2 && python -m scripts.tok_train --max-chars=100000000 && python -m scripts.base_train --depth=4 --num-iterations=5"
```

Pick a bigger GPU only when the smoke proves the need:

```bash
python scripts/modal_gpu.py --gpu=L40S -- python -m pytest tests/ -x -v
```

## GPU Cost Table (Illustrative; verify current pricing before long runs)

| GPU  | Rough $/hr | VRAM  | Use case                          |
|------|------------|-------|-----------------------------------|
| T4   | ~$0.59     | 16 GB | CUDA smoke, cheap tests           |
| L4   | ~$0.80     | 24 GB | CUDA smoke, small inference       |
| A10  | ~$1.10     | 24 GB | Small training smoke              |
| L40S | ~$1.95     | 48 GB | Larger VRAM smoke                 |
| A100 80GB | ~$2.50 | 80 GB | True 80 GB VRAM need              |
| H100 | ~$3.95     | 80 GB | Only if benchmark cost-effective  |

Typical rough costs:
- CUDA check: `<$0.01` (~30s)
- Pytest suite: `~$0.05` (~2-5 min)
- Training smoke test: `~$0.05` (~2-3 min)

Modal Sandbox CPU/memory is more expensive than Function CPU/memory, so avoid
oversizing `cpu`, `memory`, and `disk`. For training loops, the Function path is
usually cheaper and safer.

## Timeout Estimation

Always size timeout before launch. Too-low timeout wastes full run cost.

Formula:

`timeout_min = (setup_min + num_steps * step_sec / 60) * 1.5`

- Setup overhead: `~5 min` (download + tokenizer + compile warmup)
- `1.5x` margin for eval pauses and variance

Examples from an H100 benchmark. Use them only when H100 has been justified for
the workload; otherwise measure step time on the cheaper target GPU first.

- d12, 500 steps, H100: `(5 + 500*1.1/60) * 1.5 = 21` -> `--timeout=25`
- d20, 500 steps, H100: `(5 + 500*3.9/60) * 1.5 = 56` -> `--timeout=60`
- d26, 500 steps, H100: `(5 + 500*7.4/60) * 1.5 = 100` -> `--timeout=105`

Rule of thumb: for estimated runtime >20 min, set timeout explicitly.

## A/B Testing Guidance

For baseline vs treatment training comparisons, prefer `modal-gpu-experiment`
Functions with checkpointed outputs. Use this Sandbox runner only for short
smoke comparisons.

- Launch both runs in background shell jobs with explicit logs and tracked PIDs:
  ```bash
  mkdir -p /tmp/modal-runs
  python scripts/modal_gpu.py --gpu=A10 --timeout=30 -- python -m scripts.base_train ... > /tmp/modal-runs/base.log 2>&1 &
  BASE_PID=$!
  python scripts/modal_gpu.py --gpu=A10 --timeout=30 -- python -m scripts.base_train ... > /tmp/modal-runs/treatment.log 2>&1 &
  TRT_PID=$!
  wait "$BASE_PID" "$TRT_PID"
  ```
- Monitor with bounded polling (`sleep 60`, then `grep`/`tail`), not tight loops.
- Use enough tokens to avoid overfitting short-run noise.
- Use each depth's recommended batch size; under-sizing can create confounds.
- H100 eval workaround for FA3 crashes: `--force-sdpa --window-pattern=L`.
- Step-0 sanity check: baseline and treatment should match at step 0.

## Process Lifecycle and Cleanup

Killing local Python/Bash does not guarantee immediate remote sandbox stop.
Always verify and stop orphaned tasks:

```bash
python3 -m modal app list
python3 -m modal app stop <app-id>
```

Forgotten GPU sandboxes can keep billing until timeout. Every runner you create
or update should terminate in `finally` and tag/name resources so stale jobs are
findable by a sweeper.

## Limitations

- Ephemeral sandbox filesystem (no automatic write-back to local disk)
- Single-GPU by default (no distributed multi-node setup in this skill)
- First image build can take 3-5 minutes; cached afterward
- `add_local_dir` uploads repo content each run; exclude large artifacts where possible

## Troubleshooting

`module 'modal' has no attribute 'Mount'`
- You're on Modal v1.3+; use `Image.add_local_dir()`.

`'NoneType' has no attribute 'returncode'`
- `sandbox.wait()` returned `None`; read `sandbox.returncode`.

`InvalidError: Class _Mount has no constructor`
- Don't instantiate `Mount`; it is deprecated.

Sandbox timeout failures
- Keep Sandbox timeouts at or below 120 min; switch to a checkpointed Function
  for anything longer.

## Template: `scripts/modal_gpu.py`

If project runner is missing, create it from this template and customize deps:

```python
"""Run commands on a remote Modal GPU sandbox."""
import argparse
import os
import sys
import threading
import time
from datetime import datetime, timezone, timedelta


def stream_lines(stream, dest):
    for line in stream:
        dest.write(line)
        dest.flush()


def utc_expiry(seconds):
    return (datetime.now(timezone.utc) + timedelta(seconds=seconds)).isoformat()


def main():
    try:
        import modal
    except ImportError:
        print("ERROR: pip install modal && modal setup", file=sys.stderr)
        sys.exit(1)

    parser = argparse.ArgumentParser()
    parser.add_argument("--gpu", default="T4")
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--idle-timeout", type=int, default=300)
    parser.add_argument("--cpu", type=float, default=1)
    parser.add_argument("--memory", type=int, default=4096)

    try:
        sep = sys.argv.index("--")
    except ValueError:
        print("Usage: scripts/modal_gpu.py [--gpu GPU] [--timeout MINS] -- COMMAND...", file=sys.stderr)
        sys.exit(1)

    args = parser.parse_args(sys.argv[1:sep])
    timeout_seconds = min(args.timeout * 60, 2 * 60 * 60)
    idle_timeout_seconds = min(args.idle_timeout, 300)
    command = sys.argv[sep + 1:]
    if not command:
        print("ERROR: missing COMMAND after --", file=sys.stderr)
        sys.exit(1)

    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    image = (
        modal.Image.debian_slim(python_version="3.10")
        .pip_install("torch==2.9.1", extra_index_url="https://download.pytorch.org/whl/cu128")
        .pip_install("your-dep>=1.0")
        .add_local_dir(repo_root, remote_path="/app")
    )

    app = modal.App.lookup("project-sandbox", create_if_missing=True)
    sandbox = modal.Sandbox.create(
        *command,
        image=image,
        gpu=args.gpu,
        cpu=args.cpu,
        memory=args.memory,
        timeout=timeout_seconds,
        idle_timeout=idle_timeout_seconds,
        name=f"codex-gpu-smoke-{int(time.time())}",
        workdir="/app",
        app=app,
    )
    sandbox.set_tags({
        "owner": "codex",
        "purpose": "gpu-smoke",
        "expires_at": utc_expiry(timeout_seconds),
    })

    try:
        stderr_thread = threading.Thread(
            target=stream_lines,
            args=(sandbox.stderr, sys.stderr),
            daemon=True,
        )
        stderr_thread.start()
        stream_lines(sandbox.stdout, sys.stdout)
        stderr_thread.join(timeout=5)

        sandbox.wait(raise_on_termination=False)
        sys.exit(sandbox.returncode)
    finally:
        sandbox.terminate()


if __name__ == "__main__":
    main()
```
