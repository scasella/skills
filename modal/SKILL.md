---
name: modal-router
description: >
  Parent routing skill for Modal, GPU, sandbox, notebook, training, fine-tuning,
  CUDA validation, isolated execution, and remote compute work. Use before
  choosing a Modal primitive or one of the Modal child skills. Guides agents to
  prefer bounded Modal Functions for training jobs, short Sandboxes only for
  stateful debugging or isolated tests, and cost-aware GPU selection.
metadata:
  short-description: Route Modal work by primitive and cost
---

# Modal Router

Use this first for any Modal or remote-GPU task. Decide the primitive before
launching anything, then load the child skill that matches the job.

## Primitive Selection

| Use case | Default primitive | Skill |
|---|---|---|
| CPU import checks, cheap tests, data prep | Local first; Modal Function if Linux-only | `modal-basic-skills` |
| CUDA sanity check or short GPU-path test | Short bounded Sandbox runner | `modal-gpu` |
| Training, fine-tuning, sweeps, batch evals | Modal Function/job with Volumes and retries | `modal-gpu-experiment` |
| Interactive shell, profiler, SSH debugging | Short interactive GPU dev session | `modal-gpu-dev` |
| Untrusted one-shot code | Restricted Function when available; otherwise short no-GPU Sandbox | `modal-basic-skills` |
| Long predictable 10-100+ GPU-hour run | Benchmark Modal against RunPod, Lambda, Vast, or reserved/spot cloud | this skill + user confirmation |

Training means anything expected to run beyond a quick smoke, consume a dataset,
write checkpoints, or compare hyperparameters. Training should be a bounded
Function, not a long-lived Sandbox.

## Cost Preflight

Before launching any Modal GPU job, print or record:

- Primitive: Function, Restricted Function, or Sandbox
- GPU type and fallback list
- CPU, memory, disk, region, timeout, and retry count
- Estimated maximum cost and whether pricing was live-checked or approximate
- Checkpoint/cache Volume names and resume behavior
- Expected run id, app name, dashboard/log command, and cleanup command

For Codex Cloud or any automated retry system, keep attempts at `1` when the
task can launch external GPU jobs. Multiple attempts can multiply spend and
side effects.

## Default GPU Policy

- CPU first for import, lint, parser, and data-shape checks.
- T4 or L4 for CUDA availability, integration smoke, small inference, and cheap
  compatibility tests.
- A10 or L4 for small LoRA/QLoRA and short representative training.
- L40S when the real constraint is around 48 GB VRAM.
- A100 80GB when the workload truly needs about 80 GB VRAM.
- H100/H200/B200 only after a benchmark shows that speedup beats price for this
  workload.

Optimize for cheapest valid result:

```text
cost_per_successful_run =
  hourly_price * wall_clock_hours / probability_of_success
```

Do not optimize for fastest epoch unless the user explicitly asks.

## Sandbox Guardrails

Use a Sandbox only when statefulness or interactivity is the point: SSH
debugging, checking out arbitrary repos, isolated tests, or agent-generated code
that needs a container. Every Codex-created Sandbox should have:

- `timeout <= 7200`
- `idle_timeout <= 300` when using `modal.Sandbox.create`
- explicit `cpu`, `memory`, and `gpu`
- a human-readable `name`
- tags such as `owner=codex`, `purpose`, and `expires_at`
- `try/finally` cleanup that calls `terminate()`
- a follow-up cleanup check with `modal app list` / `modal app stop`

Do not use GPU Sandboxes for multi-hour training by default. Convert the command
into a Modal Function with Volumes and checkpoints.

## Function Guardrails

Training Functions should include explicit `gpu`, `cpu`, `memory`, `timeout`,
`retries`, and Volumes for model cache, dataset cache, checkpoints, and final
artifacts. Avoid `min_containers`, `buffer_containers`, and long
`scaledown_window` unless the user chooses to pay for warm capacity.

Long training should checkpoint periodically, resume from the latest checkpoint,
and exit cleanly. Start with a staged funnel:

1. CPU import/config test.
2. Tiny GPU smoke on T4/L4/A10.
3. 1-5 percent data run or `--max_steps`/`--limit_train_batches`.
4. First-checkpoint comparison.
5. Full run only for the best candidate.

## External Provider Check

For long, predictable runs, ask whether to benchmark another provider before
committing Modal spend. Compare total cost, not headline GPU price: startup
time, storage, network egress, failed attempts, interruption risk, and human
debug time all count.
