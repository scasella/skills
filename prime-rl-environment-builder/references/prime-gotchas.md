# Prime Gotchas

## Account And Ownership
- Your Prime username must exist before you can publish under it.
- If you do not have a team configured, there is no team-owner fallback.
- Personal-account creation can behave differently from collaborator or team paths.
- A publish that fails with an explicit `--owner <personal-slug>` may still succeed when you omit `--owner` and let Prime use the authenticated personal account.

## Pulled Source Is Not A Perfect Mirror
- `prime env pull` can omit files that exist in the GitHub repo or local checkout.
- Do not make source installs depend on files that may be absent after pull.
- Prime-pulled directories may also contain extra files like logs or `.prime` metadata; installability should survive that.

## Metadata Expectations
- Current Prime integration tests can require a nonstandard `project.tags` field in `pyproject.toml`.
- A placeholder description can fail metadata tests even if everything else installs.
- SPDX-style license metadata is safer than a `license = { file = ... }` stanza when pulled-source contents are incomplete.

## Release Synchronization
- After publishing a new version to Prime Hub, sync the version metadata back to GitHub if the repo should reflect the released state.
- Re-run pulled-source install checks after every metadata change, not just after code changes.
- Ignore `.prime/` in the public repo so local publish metadata does not leak into source control.

## Eval And Publish Discipline
- Do not treat local `vf-eval` as proof that uploaded `prime eval run` will succeed.
- Run a smoke eval first to catch packaging, load-name, or provider issues cheaply.
- Inspect sample-level failures before changing reward code; some issues are packaging or env-arg problems, not benchmark flaws.
