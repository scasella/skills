---
name: modal-gpu-experiment
user-invocable: true
description: >
  Training apps, experiment patterns, and persistent storage on Modal.
  Write single-GPU and multi-node training jobs with volumes for data
  and checkpoints, secrets for W&B/HuggingFace, and fault tolerance
  via retries and checkpoint auto-resume. Use when you need to run
  training, fine-tuning, sweeps, or batch experiments on Modal GPUs.
  Prefer this Function/job skill over GPU Sandboxes for repeated training loops.
---

# Modal Experiments

Run training jobs and experiments on Modal GPUs — from single-GPU fine-tuning
to multi-node distributed training with RDMA. Use bounded Modal Functions:
bake your code into the image, mount Volumes for data/cache/checkpoints, add
secrets, set retries, resume from checkpoints, and exit.

For general Modal platform usage (app structure, function types, CLI, deployment), see the `modal-basic-skills` skill.

## Cost Rules

- Training belongs in Functions/jobs, not GPU Sandboxes.
- Before launch, print GPU/fallbacks, CPU, memory, disk, timeout, retries,
  Volume names, expected max cost, and cleanup/log commands.
- Default to CPU/T4/L4 smoke tests, then A10 or L4 for small training, L40S for
  48 GB VRAM, A100 80GB for true 80 GB VRAM, and H100/H200/B200 only after
  benchmark evidence or explicit user direction.
- Avoid `min_containers`, `buffer_containers`, and long `scaledown_window`
  unless the user chooses to pay for warm capacity.
- Optimize for cheapest successful run, not fastest epoch.

Use a staged funnel: CPU import test, tiny GPU smoke, 1-5 percent data or
`--max_steps`, first-checkpoint comparison, then full training only for the best
candidate.

## Quick Reference

### Training App Pattern

A Modal training Function can live in a single Python file:

```python
import modal

app = modal.App("my-training")

data_volume = modal.Volume.from_name("training-data", create_if_missing=True)
ckpt_volume = modal.Volume.from_name("training-checkpoints", create_if_missing=True)

image = (
    modal.Image.from_registry("nvidia/cuda:12.6.0-devel-ubuntu22.04", add_python="3.12")
    .pip_install("torch", "transformers", "datasets", "accelerate", "wandb")
    .add_local_file("train.py", remote_path="/root/train.py", copy=True)
    .add_local_dir("src/", remote_path="/root/src", copy=True)
)

@app.function(
    image=image,
    gpu="A10",
    cpu=4,
    memory=16 * 1024,
    timeout=60 * 60 * 2,
    volumes={"/data": data_volume, "/checkpoints": ckpt_volume},
    secrets=[modal.Secret.from_name("wandb-secret")],
    retries=modal.Retries(max_retries=3),
)
def train(config: str = "configs/default.yaml"):
    import subprocess
    subprocess.run(["python", "/root/train.py", "--config", config], check=True)

@app.local_entrypoint()
def main(config: str = "configs/default.yaml"):
    train.remote(config=config)
```

```bash
modal run my_train.py
modal run my_train.py --config configs/large.yaml
```

### Key Patterns

- **`add_local_file` / `add_local_dir`**: Bake code into the image. **Use `copy=True`** if you chain `.run_commands()` after.
- **Volumes**: Mount persistent storage for data and checkpoints. Data survives across runs.
- **Secrets**: `modal.Secret.from_name(...)` for W&B, HuggingFace tokens, etc.
- **Retries + auto-resume**: `modal.Retries(max_retries=N)` combined with checkpoint detection for fault-tolerant training.
- **Explicit resources**: Set `gpu`, `cpu`, `memory`, `timeout`, and `retries`; do not rely on defaults for GPU jobs.
- **No warm pools by default**: avoid `min_containers`, `buffer_containers`, and long `scaledown_window`.

### Persistent Storage

```bash
# List/download/upload via CLI
modal volume ls training-data /
modal volume get training-checkpoints /my-experiment/latest.pt ./latest.pt
modal volume put training-data ./dataset.tar.gz /dataset.tar.gz
```

See ./references/volumes.md for data caching, checkpoint patterns, and `volume.commit()`.

### Multi-Node Training

For models that truly need more than 8 GPUs, use `@modal.experimental.clustered`
with RDMA for up to 3,200 Gbps inter-node bandwidth. Treat this as an explicit
large-run path, not a default.

```python
@app.function(
    gpu=f"H100:8",
    cpu=16,
    memory=128 * 1024,
    timeout=60 * 60 * 24,
    experimental_options={"efa_enabled": True},
)
@modal.experimental.clustered(size=2, rdma=True)
def train(config: str):
    cluster_info = modal.experimental.get_cluster_info()
    # Use cluster_info.rank, cluster_info.container_ips for torchrun
```

See ./references/training.md for full examples including NCCL configuration and torchrun integration.

### Compute Options

See ./references/compute.md for the full GPU table and selection guide. Quick guide:
- **Smoke/import**: CPU, `T4`, or `L4`
- **Small LoRA/QLoRA or short training**: `A10` or `L4`
- **48 GB VRAM**: `L40S`
- **80 GB VRAM**: `A100-80GB`
- **H100/H200/B200**: only after benchmark evidence or explicit user direction

## References

- ./references/training.md — Full training guide (single-node, multi-node, data loading)
- ./references/volumes.md — Persistent storage patterns
- ./references/compute.md — GPU options and selection guide

## See Also

- For interactive debugging before writing a training Function: use the `modal-gpu-dev` skill
- For running experiments in parallel across multiple agents: use the `sub-agents` skill
