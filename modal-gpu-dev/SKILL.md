---
name: modal-gpu-dev
user-invocable: true
description: >
  Short interactive GPU sessions on Modal with SSH access for debugging,
  profiling, and prototyping. Use only when stateful hands-on GPU access is
  needed; prefer Modal Functions for training, fine-tuning, sweeps, and batch
  jobs. Defaults should be cost-aware, short-lived, and explicitly cleaned up.
---

# GPU Debugging

Interactive GPU containers on Modal with SSH access. Use for debugging,
profiling, prototyping, or any work where you need hands-on access to a GPU
environment. Do not use this skill for normal training loops; once the command
is understood, move it to a bounded Modal Function via `modal-gpu-experiment`.
Your workspace is persisted to a Modal Volume and synced every 30 seconds.

For general Modal platform usage (app structure, function types, CLI, deployment), see the `modal-basic-skills` skill.

## Cost Rules

- Default to CPU, T4, L4, or A10 unless the workload proves it needs more VRAM.
- Use L40S for roughly 48 GB VRAM and A100 80GB for true 80 GB needs.
- Use H100/H200/B200 only after benchmark evidence or explicit user direction.
- Keep sessions short: this tool is capped at 2 hours; kill it sooner when done.
- Before launch, state GPU, CPU, memory, timeout, expected maximum cost, sandbox
  id, and the cleanup command.
- After launch or interruption, verify cleanup with `modal app list`; stop stale
  apps with `modal app stop <app-id>`.

## Quick Reference

### Launch a Sandbox

```bash
# Launch with specific GPU (runs in background)
_SANDBOX_GPU=A10 python -m modal run modal-gpu-dev/tools/gpu_sandbox.py \
  --key-path ~/.ssh/id_ed25519.pub --gpu A10 --sandbox-id my-sandbox > /tmp/sandbox.log 2>&1 &

# Wait for SSH info (written to volume — reliable, not buffered)
while true; do
  modal volume get gpu-sandbox-workspace /ssh-info/my-sandbox.json /tmp/ssh-info.json 2>/dev/null && break
  sleep 3
done
HOST=$(python3 -c "import json; d=json.load(open('/tmp/ssh-info.json')); print(d['host'])")
PORT=$(python3 -c "import json; d=json.load(open('/tmp/ssh-info.json')); print(d['port'])")

# SSH in (available immediately — sshd starts before volume sync)
ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
  -i ~/.ssh/id_ed25519 -p $PORT root@$HOST "nvidia-smi"
```

Sessions auto-terminate after 2 hours. Treat that as a backstop, not the normal
cleanup path.

### SSH Commands

```bash
# Run a command
ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
  -o LogLevel=ERROR -i ~/.ssh/id_ed25519 -p $PORT root@$HOST "nvidia-smi"

# Upload/download files
scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
  -i ~/.ssh/id_ed25519 -P $PORT ./local_file.py root@$HOST:/tmp/
scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
  -i ~/.ssh/id_ed25519 -P $PORT root@$HOST:/tmp/results.json ./

# Rsync a directory
rsync -avz --exclude .git/ --exclude __pycache__/ --exclude .venv/ \
  -e "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i ~/.ssh/id_ed25519 -p $PORT" \
  ./my_code/ root@$HOST:/tmp/my_code/
```

### Workspace Persistence

The workspace at `/root/workspace` is backed by a Modal Volume (`gpu-sandbox-workspace`) and synced every 30 seconds. Data persists across sandbox restarts.

```bash
# List files on the volume
modal volume ls gpu-sandbox-workspace /workspace

# Download/upload via CLI
modal volume get gpu-sandbox-workspace /workspace/results.json ./results.json
modal volume put gpu-sandbox-workspace ./data.tar.gz /workspace/data.tar.gz
```

### Compute Options

Modal offers GPUs from T4 (16 GB) to B200 (192 GB), with up to 8 GPUs per
container. Pick the cheapest GPU that can answer the debugging question.

See ./references/compute.md for the full GPU table, selection guide, and CUDA details.

### Development Workflow

1. Launch a short session with the cheapest GPU that can reproduce the issue
2. Upload your code via scp/rsync
3. SSH in and iterate: run, debug, profile
4. Once the code works, write a proper Modal training Function (see the `modal-gpu-experiment` skill)
5. Kill the session and verify no Modal app is still running

## References

- ./references/development.md — Full development workflow, environment details, use cases
- ./references/compute.md — GPU options and selection guide

## See Also

- For writing training Functions/jobs: use the `modal-gpu-experiment` skill
- For running multiple sandboxes in parallel (multi-agent): use the `sub-agents` skill
