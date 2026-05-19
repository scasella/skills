---
name: prime-rl-environment-builder
description: Design, implement, harden, package, publish, and validate Prime Intellect `verifiers` / RL environments. Use when creating a new Prime RL environment, tightening reward design, adding realistic task packs or private holdouts, preparing GitHub and Prime Hub release metadata, debugging `prime env push` or `prime eval run`, or fixing pulled-source integration failures.
---

# Prime RL Environments

## Overview
Prime RL environments are benchmark products, not just Python files. Use this skill when you need to keep environment design, anti-gaming hardening, public packaging, Prime Hub publish, and official eval validation aligned on the real user path.

## Core Rules

Do:
- Restate the real user path and concrete acceptance checks before editing.
- Verify current `prime` CLI behavior with `prime --version` and `prime ... --help` before relying on exact flags or owner semantics.
- Validate the full release path: local tests, build, pulled-source install, `prime env info/install`, and uploaded evals.
- Validate raw model payloads before canonicalization and add adversarial reward-order tests.
- Keep the public interface stable unless the benchmark thesis requires a change.
- Stop on the first Prime-specific failure and report the exact failing command plus the key output.

Do NOT:
- Claim release success from local `pytest` or `vf-eval` alone.
- Let normalization hide malformed outputs.
- Publish packages that depend on source files Prime pull may omit.
- Push internal docs, private holdouts, eval artifacts, or `.prime/` metadata in the public repo.
- Add realism features without re-validating the incentives and score signal.

## Workflow

1. Ground the repo and the real path
   - Find `load_environment()`, package name, tool loop, eval commands, and public repo shape.
   - Confirm current Prime CLI semantics before assuming command flags or owner behavior.
   - Write acceptance checks that match how the user will actually publish and run evals.

2. Design or audit the benchmark thesis
   - State what behavior the environment is trying to train.
   - Check whether the task loop, tools, and reward terms actually support that behavior.
   - Prefer novelty with accountability: evidence grounding, feasibility, and a discriminative experiment.

3. Harden rewards and tests
   - Validate raw payloads before normalization.
   - Gate grounding and baseline differentiation on actual tool exposure.
   - Use opaque IDs when guessable IDs leak reward.
   - Add citation-precision terms and feasibility floors where novelty can be gamed.
   - Add adversarial tests that assert reward ordering, not just one-off scalar values.

4. Prepare the public repo and package metadata
   - Keep the public repo minimal and installable.
   - Make `pyproject.toml` Prime-safe, including metadata required by current integration tests.
   - Ignore `.prime/`, internal notes, holdouts, outputs, caches, and build artifacts.
   - Keep the README public-facing and explicit about install and eval commands.

5. Publish to GitHub and Prime Hub
   - Push only the public file set to GitHub.
   - Publish to Prime Hub from the tested repo state.
   - Treat owner and visibility behavior as unstable; verify against the current CLI and actual responses.

6. Validate pulled-source install and official evals
   - Run `scripts/check_prime_env_integration.py`.
   - Confirm `prime env info`, `prime env install`, and a pulled-source install all work.
   - Run an uploaded smoke eval first, then the full official evals.
   - Inspect sample-level outputs, not just aggregate rewards.

7. Triage Prime-specific failures
   - Package/install failures: inspect pulled source contents, `pyproject.toml`, and build requirements.
   - Publish failures: check `prime whoami`, owner semantics, visibility, and repo state.
   - Eval failures: inspect env args, model/provider path, and sample-level failures before changing code.

## Use The References
- Open `references/design-and-hardening.md` for environment thesis, reward design, anti-gaming, and task-pack structure.
- Open `references/release-and-evals.md` for packaging, metadata, GitHub release, Prime publish, and official eval execution.
- Open `references/prime-gotchas.md` when Prime behavior is surprising or a previously working publish/install path regresses.

## Use The Helper Script
Run `scripts/check_prime_env_integration.py` before or after publish whenever installability, metadata completeness, or pulled-source behavior is in doubt. Use `--env-dir` for local repos and `--env-id` for published Hub envs.

## Example Triggers
- “Create a new Prime verifiers environment for mechanistic discovery.”
- “Publish this environment to Prime Hub and run official evals.”
- “Why does `prime env push` fail?”
- “Fix the Prime integration test for this environment.”
- “Add a realistic task pack and holdout path.”
