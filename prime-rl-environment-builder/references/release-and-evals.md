# Release And Evals

## Minimal Public Repo Surface
- Keep the public repo installable and easy to audit.
- Typical public set:
  - environment code
  - `README.md`
  - `pyproject.toml`
  - tests
  - `LICENSE` when the package or repo needs it publicly
  - lockfile if it is part of the project workflow
  - minimal ignore or config files
- Keep internal handoff docs, private holdouts, eval artifacts, and local metadata out of the public repo.

## Ignore Rules
Add ignores for:
- `.prime/`
- private holdout directories
- local outputs and logs
- build artifacts like `dist/`
- caches like `.pytest_cache/`
- internal markdown or design notes not meant for public release

## Prime-Safe `pyproject.toml`
Current Prime integration expectations can require:
- `project.name`
- `project.version`
- `project.description`
- `project.tags`
- `project.readme`
- `project.license`
- runtime dependencies

Guidance:
- Use a non-placeholder description.
- Prefer SPDX-style license metadata when source pulls may omit local files used by `license = { file = ... }`.
- Keep metadata synchronized with the published Prime version after release.

## Local Release Gate
Run these before any publish:

```bash
uv run pytest -q
uv build --out-dir dist
uv run twine check dist/*
```

Then run small local evals that mirror the real modes you intend to release:

```bash
uv run vf-eval <env-name> -n 2 -r 1 --debug
uv run vf-eval <env-name> -n 2 -r 1 -a '{"task_mode":"surrogate_realistic"}' --debug
```

Use the smallest safe subset first. Only scale up after the smoke path passes.

## GitHub Release Flow
- Stage only the public file set.
- Verify no internal docs, outputs, `.prime/`, or build artifacts are staged.
- Push the tested repo state to GitHub.
- Confirm the remote commit matches what you validated locally.

## Prime Hub Flow
Before publishing:

```bash
prime whoami
prime --version
prime env push --help
prime eval run --help
```

Then publish and validate:

```bash
prime env push --path . --name <env-name> --visibility PUBLIC
prime env info <owner>/<env-name>
prime env install <owner>/<env-name>
```

Treat owner semantics as unstable. Verify what the current CLI accepts instead of assuming an older flow still works.

## Official Eval Flow
- Run an uploaded smoke eval first.
- Then run the full official benchmark.
- Capture eval IDs and any URLs printed by the CLI.
- Inspect samples, not just aggregate reward tables.
- Compare public-dev-pack and private-holdout results before declaring the environment robust.

Example pattern:

```bash
prime eval run <owner>/<env-name> --model <model> --num-examples 2 --rollouts-per-example 1 --debug
prime eval run <owner>/<env-name> --model <model> --num-examples 20 --rollouts-per-example 4 --debug
prime eval samples <eval-id>
prime eval list
```
