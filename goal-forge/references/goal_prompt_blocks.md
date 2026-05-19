# Goal Prompt Blocks

Use this structure for `GOAL.md`.

```xml
<goal>
[What the task produces. Specific, measurable, and execution-oriented.]
</goal>

<context>
[Files to read first, systems to inspect, and discovery commands if exact files are unknown.]
</context>

<constraints>
[Architecture rules, non-goals, risk boundaries, and anti-pattern fences.]
</constraints>

<done_when>
[Concrete user-approved completion criteria. Tests, artifacts, behavior, and explicit non-regression checks.]
</done_when>

<workflow>
[Step-by-step execution order. Identify which reads/searches can run in parallel and where verification gates belong.]
</workflow>

<verification_loop>
[Commands and manual checks to run after major changes. Include fallback instructions when a check cannot run.]
</verification_loop>

<execution_rules>
[Stable Codex working rules for repo hygiene, edits, testing, and final communication.]
</execution_rules>

<output_contract>
[Expected final artifacts, final response shape, and completion signal.]
</output_contract>
```

Save only the XML block body in `GOAL.md`. The user can run or paste it after the Codex `/goal` command; do not include a standalone `/goal` line in the file unless the user explicitly asks for a paste-ready command transcript.

## Block Guidance

`<goal>` should describe the deliverable, not the process. Avoid vague verbs like "improve" unless paired with measurable behavior.

`<context>` should make the first turn efficient. Prefer concrete files. If the exact files are unknown, include discovery commands such as `rg "symbol"` or `rg --files`.

`<constraints>` should prevent shortcuts that could pass tests while violating intent. Include non-goals here.

`<done_when>` is the termination contract. It must be concrete enough that the agent can decide whether to call the task complete.

`<workflow>` should sequence the work in phases: inspect, plan, implement, verify, refine, final review.

`<verification_loop>` should include focused checks first, then broad checks. If manual QA is required, specify what evidence is sufficient.

`<execution_rules>` carries stable agent behavior, such as preserving unrelated changes and using `apply_patch`.

`<output_contract>` should say what files or artifacts must exist and how concise the final response should be.
