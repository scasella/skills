# Design And Hardening

## Benchmark Thesis
- Train novelty with accountability, not novelty alone.
- The environment should reward a model for searching the design space, grounding claims in surfaced evidence, distinguishing itself from known baselines, and proposing a falsifiable next experiment.
- Avoid benchmarks that only reward plausible prose or symbolic novelty divorced from feasibility.

## Hybrid Synthetic Lab Pattern
- Use a middle ground between a toy puzzle and open-web judging.
- Keep tasks structured and cheap enough for RL rollouts, but rich enough to reward evidence use and experimental thinking.
- A strong shape is:
  - synthetic or curated research brief
  - components or interventions to combine
  - evidence cards available through tools
  - known baseline ideas available through tools
  - one structured JSON submission

## Public Interface Discipline
- Keep `load_environment()` stable unless the benchmark thesis requires a public API change.
- Preserve tool names when possible so reward or realism work does not constantly break downstream evals.
- Add optional parameters for new task sources instead of replacing defaults:
  - bundled realistic task modes
  - `domain_filter`
  - external `task_pack_path` for private holdouts

## Reward Hardening Rules
- Validate the raw completion payload before canonicalization.
- Treat normalization as cleanup only, never as the reason malformed outputs pass schema checks.
- Gate grounding on actual evidence exposure:
  - only surfaced or opened evidence should count
  - guessed IDs should not earn credit
- Gate baseline differentiation on actual baseline exposure:
  - `distinguishes_from` should only score when the referenced idea was available through the tool loop
- Use opaque, per-task IDs for evidence and baselines when sequential IDs are guessable.
- Add citation precision so “cite everything” performs worse than focused evidence use.
- Add a feasibility floor for novelty and diversity so impossible but structurally unusual ideas do not win.

## Testing Strategy
- Write adversarial tests that check orderings, not just single numeric values.
- Useful reward-order assertions:
  - well-grounded > citation stuffing
  - retrieved-evidence > guessed-evidence
  - seen-baseline > unseen-baseline
  - feasible-novel > infeasible-novel
  - valid-schema > malformed
- Keep positive-path tests too:
  - valid JSON parses once and caches correctly
  - a strong proposal can earn non-zero non-format rewards

## Realism Without Losing Control
- Use bundled realistic dev packs for public iteration.
- Use private holdout packs outside the public repo for release gating.
- Keep the final answer schema comparable across synthetic and realistic modes so model comparisons remain interpretable.
- Prefer one well-built realistic track over many shallow “realistic” domains.

## Common Failure Modes
- Reward collapse because parsing caches `None` before parsing ever happens.
- Grounding credit for citations the model never retrieved.
- Schema validation performed after canonicalization.
- Novelty terms overpowering feasibility.
- Public task packs becoming the whole benchmark because no private holdout exists.
