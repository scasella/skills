# Skills

Personal Codex skill collection for reusable workflows, research writeups, Modal work, Tinker work, Prime Intellect environment work, and HTML artifacts.

## Contents

| Skill | Purpose |
| --- | --- |
| `html-artifact` | Produce polished, self-contained HTML deliverables instead of long markdown artifacts. |
| `goal-forge` | Turn rough coding ideas into executable specs and Codex `/goal` prompts. |
| `modal` | Route Modal, GPU, sandbox, notebook, training, fine-tuning, and CUDA requests to the right workflow. |
| `modal-alias` | Alias skill for the Modal router. |
| `modal-basic-skills` | Foundational Modal platform knowledge for auto-research agents. |
| `modal-gpu` | Run short, bounded commands on remote Modal GPU sandboxes for GPU validation. |
| `modal-gpu-dev` | Use short interactive GPU sessions on Modal with SSH access for debugging and prototyping. |
| `modal-gpu-experiment` | Build Modal training apps, experiment patterns, and persistent storage workflows. |
| `research-blog` | Turn experimental results into self-contained HTML research blog posts. |
| `prime-rl-environment-builder` | Design, harden, package, publish, and validate Prime Intellect RL environments. |
| `tinker-core` | Core Tinker API setup, model selection, SDK, CLI, and hyperparameter guidance. |
| `tinker-debug` | Diagnose Tinker performance, renderer, export, service, and error issues. |
| `tinker-dev` | Contribute to `tinker-cookbook`, create recipes, and run development checks. |
| `tinker-ops` | Manage Tinker checkpoints, weight export, logging, metrics, and evaluation. |
| `tinker-preferences` | Run DPO, RLHF, preference data, and reward-model workflows with Tinker. |
| `tinker-rl` | Build and run GRPO, verifiable reward, custom environment, and multi-turn RL workflows with Tinker. |
| `tinker-sft` | Run supervised fine-tuning, chat fine-tuning, rendering, completion, and distillation workflows with Tinker. |

Each skill directory is intended to be self-contained: `SKILL.md` is the entry point, and sibling `references/`, `assets/`, `scripts/`, `agents/`, and `evals/` directories provide supporting material where present.

## Installation

Copy a skill directory into your Codex skills directory:

```bash
cp -R tinker-core ~/.codex/skills/
```

Or copy the full collection:

```bash
rsync -a --exclude .git --exclude .DS_Store ./ ~/.codex/skills/
```

## Public-Repo Notes

This repository should not contain API keys, private SSH keys, credentials, model weights, run logs, local caches, or experiment scratch data. The `.gitignore` blocks common local and credential files.

No repository-wide license is declared here. Individual skill directories may include their own license files.
