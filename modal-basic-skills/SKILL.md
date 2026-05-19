---
name: modal-basic-skills
description: >
  Foundational Modal platform knowledge for auto-research agents. Covers app
  structure, function types, CLI usage, deployment patterns, development
  workflow, and cost-aware primitive selection. This skill auto-triggers when
  code imports `modal` and provides the base layer that the GPU-specific
  research skills build on.
---

# Modal Basics for Auto-Research

Foundational Modal platform knowledge for research agents. Covers how Modal apps work, the CLI, and development patterns. The GPU-specific skills (`modal-gpu-dev`, `modal-gpu-experiment`, `sub-agents`) build on these basics.

Modal is a serverless platform for AI/ML workloads — scalable compute (including GPUs) with minimal configuration, pay only for what you use.

# Cost-first primitive selection

Before launching Modal work, choose the cheapest primitive that satisfies the
use case:

| Use case | Primitive |
|---|---|
| Training, fine-tuning, batch evals, sweeps | Modal Function/job with Volumes and retries |
| CUDA sanity check or short GPU-path test | Short bounded Sandbox runner |
| Interactive shell, SSH debugging, profiling | Short interactive GPU dev session |
| Stateless untrusted snippet | Restricted Function when available |
| Long predictable 10-100+ GPU-hour run | Benchmark Modal against a pod/marketplace provider |

Do not use GPU Sandboxes as the default training environment. Sandboxes are for
stateful or interactive work; training should run as a bounded Function that
exits.

Before any GPU launch, report the primitive, GPU, CPU, memory, disk, timeout,
retry count, approximate maximum cost, cache/checkpoint Volume names, and cleanup
command. Keep external-job-launching Codex Cloud attempts at `1`.

Avoid cost multipliers unless intentionally chosen: over-requested CPU/memory or
disk, region pinning, non-preemptible execution, `min_containers`,
`buffer_containers`, and long `scaledown_window` values.

# Documentation

Modal's documentation is outlined at https://modal.com/llms.txt.

The docs are divided into three sections:

- Fetch _Guide_ pages for in-depth explanations of Modal features, primitives, and workflows
- Fetch _Examples_ pages to see how different AI applications look on Modal
- Fetch _API Reference_ pages for signatures and docstrings for components of the Python SDK

For broader context, https://modal.com/llms-full.txt aggregates all docs in a single very large file. Do not read this into your main context.

# Getting up to date

You have significant knowledge about Modal from your training data but may not be aware of new features or recent changes to the API. Fetching relevant docs while planning can help you discover the most up-to-date way to accomplish a task on Modal.

The Modal CLI provides a `modal changelog` command that can also be useful for learning about recent changes. There are several options for querying change sets. E.g., running `modal changelog --since DATE` will show all changes made between that date (e.g., your knowledge cutoff) and the release of the SDK version that is in use.

Run `modal --version` to see the SDK version that is in use. Note that the online docs may reference features that are available only in recent SDKs.

# Using the CLI

The `modal` CLI can be used to run or deploy code, manage resources, and observe running Apps. It is a key tool for interacting with Modal.

Run `modal --help` to see all available CLI commands.

You can see more detailed information about each command by running `modal [command] --help`. If you are unsure of how to accomplish a task through the CLI (or if you get an error when trying), read the `--help` rather than guessing.

Tip: most CLI commands accept a `--json` flag to make their output more easily parseable, e.g. with `jq`.

# More information

When authoring Modal App code, the following references will be useful:

- ./references/app-structure.md
- ./references/function-types.md
- ./references/development-workflow.md
