# Use-case playbooks

Match the user's prompt to one of the patterns below. Each pattern lists the sections to include and the components from `components.md` to reach for. Using the right skeleton is the #1 way to avoid generic-feeling output.

## How to choose

| Prompt signal | Pattern |
|---|---|
| "plan", "spec", "scope", "design doc", "implementation plan" | **Spec / plan** |
| "brainstorm", "options", "approaches", "compare directions", "N variants of" | **Exploration** |
| "review this PR", "code review", "explain this diff", "writeup of this change" | **Code review / PR writeup** |
| "explain how X works", "I don't understand X", "what is our X?", "feature explainer" | **Research explainer** |
| "design system", "components", "tokens", "variants", "states of" | **Design system / variants** |
| "prototype an animation", "tune this transition", "with sliders / knobs" | **Animation sandbox** |
| "build me an editor / triage / configurator for", "prioritize these tickets", "edit this config visually" | **Custom editor** |
| "weekly status", "retro", "shipped this week", "team update" | **Status report** |
| "incident report", "post-mortem", "what happened with X outage" | **Incident timeline** |
| "slide deck", "presentation", "5-slide overview" | **Slide deck** |

If the prompt straddles two patterns, pick the one with more specific structural requirements. Don't combine them.

---

## Pattern: Spec / plan

### Sections (in order)

1. Masthead (eyebrow "Spec · v1" or "Implementation plan", h1 with italic emphasis, one-line lead).
2. Prompt-box quoting the original ask, OR a `.callout` TL;DR — pick one, not both.
3. **Goals / non-goals** as a two-column grid.
4. **Approach** — prose + one architecture diagram (`svg-diagrams.md` → architecture).
5. **Data flow** or **state machine** — one diagram.
6. **Milestones / timeline** — `.timeline` component.
7. **Risks** — a list of `.card`s with risk tags (high/med/low) and brief mitigations.
8. **Open questions** — short bulleted list as a final `.callout`.

### Components to reach for

- masthead, prompt-box, callout, card, timeline, risk-tag, SVG architecture diagram, code block for one or two critical snippets.

### Anti-patterns specific to this pattern

- Don't include a Gantt-style chart. Use the timeline component (vertical) instead.
- Don't add a "metrics we will track" section unless the user mentioned metrics. It is filler.
- Don't generate fake code samples. If you don't have the real code, use a "schema" callout instead.

### Example prompt

> Create a thorough implementation plan for comment threads on task cards. Be sure to make some mockups, show data flow and add important code snippets I might want to review.

---

## Pattern: Exploration / N approaches

The "show me 4 ways to do this" page. Side-by-side grid of options, each labeled with its tradeoff.

### Sections

1. Masthead.
2. Prompt-box.
3. **Side-by-side comparison grid** (`.compare` / `.option`) — typically 3–6 options.
4. **Decision matrix** (optional) — a CSS-Grid table comparing options against criteria.
5. **My recommendation** — final `.callout` with `border-left-color: var(--clay)`.

### Components

- masthead, prompt-box, compare grid with `.option`, tradeoff eyebrows in clay mono, CSS-Grid table.

### Rules

- **Each option labels its tradeoff first**, in mono clay uppercase, *before* the option name. This is the single most useful affordance for the reader: "what is this option optimizing for?"
- Options should be **distinctly different**, not three variants of the same idea. If the user asks for 4 and you can only generate 3 meaningfully distinct ones, generate 3.
- Pre-rank or pre-recommend if asked. Don't be falsely neutral.

### Example prompt

> I'm not sure what direction to take the onboarding screen. Generate 6 distinctly different approaches — vary layout, tone, and density — and lay them out as a single HTML file in a grid so I can compare them side by side. Label each with the tradeoff it's making.

---

## Pattern: Code review / PR writeup

### Sections

1. Masthead with PR title and metadata (mono branch name, author avatar, file count badge).
2. **TL;DR callout** — what this PR does in 2 sentences.
3. **Files changed** — small CSS-Grid list with file paths in mono and inline `+N -M` chips.
4. **Annotated diff** — the actual changes rendered with `.diff` component, with `.bubble` comment bubbles attached to specific lines for blocking comments / nits / suggestions.
5. **Why this change** — prose section.
6. **Risks / what could break** — `.card`s with risk-tags.
7. **Reviewer focus areas** — a callout naming 2–3 things the reviewer should pay special attention to.

### Components

- masthead, callout, avatar, badge, risk-tag, diff, bubble, row-list for the file index.

### Rules

- **Render the actual diff inline.** Don't gesture at it ("see the changes in `foo.ts`"). Show it.
- Severity-color the bubbles: `.blocking` (rust), `.suggest` (amber), `.nit` (steel).
- File paths are always in mono. Branch names too.

### Example prompt

> Help me review this PR by creating an HTML artifact that describes it. I'm not very familiar with the streaming/backpressure logic so focus on that. Render the actual diff with inline margin annotations, color-code findings by severity.

---

## Pattern: Research explainer

The "explain how X works" page. Optimize for someone reading it once. Layout uses a sticky TOC sidebar.

### Sections

1. Masthead.
2. Prompt-box quoting the question.
3. **TL;DR callout** — the 3-sentence answer.
4. **Two-column layout**: sticky TOC sidebar + main content.
5. Main content sections, each with a serif h2:
   - **Overview** with one diagram (flow, architecture, or ring).
   - **The key code paths** — 3–4 `<pre class="code">` blocks with inline annotations.
   - **Tabbed sample inputs** (optional) — for showing how the system behaves on different inputs.
   - **Gotchas** — `<details>` collapsibles, one per gotcha.
   - **FAQ** — another set of `<details>`.

### Components

- masthead, prompt-box, callout, TOC sidebar, code block, SVG diagram (flowchart or ring), details collapsibles.

### Rules

- Optimize for **read-once**. Aggressively cut anything that isn't load-bearing.
- The TL;DR must work as a standalone summary — if the reader stops there, they should still know the answer.
- One main diagram, not five. Choose the one that carries the most weight.

### Example prompt

> I don't understand how our rate limiter actually works. Read the relevant code and produce a single HTML explainer page: a diagram of the token-bucket flow, the 3–4 key code snippets annotated, and a "gotchas" section at the bottom. Optimize it for someone reading it once.

---

## Pattern: Design system / variants

### Sections

1. Masthead.
2. **Color palette** — a strip of color swatches, each with hex code in mono and a copy-on-click.
3. **Type scale** — h1/h2/h3/body/caption stacked, each labeled with its size and stack name in mono.
4. **Spacing tokens** — visual rectangles sized to 4/8/12/16/24/32/48.
5. **Components in all states** — a contact sheet: button (default, hover, primary, disabled), badge (all variants), card, etc.
6. **Don'ts** — `.callout danger` examples of patterns to avoid.

### Components

- masthead, all the component patterns rendered side-by-side, copy-to-clipboard buttons on each token.

### Rules

- Every token should be one-click copyable. The whole point of a design system page is that downstream artifacts copy values from it.

### Example prompt

> Make a design-system reference for our internal apps: palette, type scale, spacing, button + badge + card variants. Copy-on-click for every token.

---

## Pattern: Animation sandbox

A live preview + sliders for tuning a transition. The output of "tuning" is parameters that can be copied back into Claude.

### Sections

1. Masthead.
2. **Live preview area** — a small playable demo at the top.
3. **Controls** — sliders, dropdowns, color pickers. Bound via CSS variables.
4. **Copy as CSS** / **Copy as params** button — exports the current settings.
5. **Prompt to paste back into Claude** — generated text that includes the current values, with a copy button.

### Components

- masthead, button (copy variant), slider control, `<output>` element for live values.

### Interactivity

- Use CSS custom property swapping: `root.style.setProperty('--ease', value)` from slider input.
- Use `requestAnimationFrame` debouncing if rendering is expensive.

### Rules

- The export at the bottom is mandatory. A sandbox that doesn't round-trip back into Claude is a half-finished feature.
- Use one main playable element, not a wall of them.

### Example prompt

> I want to prototype a new checkout button. When clicked it does a play animation and then turns purple. Create a HTML file with several sliders and options for me to try different options, with a copy button to copy the parameters that worked well.

---

## Pattern: Custom editor

The bespoke editing UI for a specific piece of data. Triage boards, feature flag editors, prompt tuners. NOT a SaaS product — a throwaway editor for this one job.

### Sections

1. Masthead with a brief description of what's being edited.
2. **Editor surface** — kanban, form, side-by-side, drag-and-drop — chosen for the data.
3. **Sticky toolbar / footer** with export buttons.
4. **Optional: warnings / validation hints** as inline `.callout warning`.

### Components

- masthead, draggable cards, row-list, button (multiple copy variants), inline `.bubble`s for warnings.

### Rules

- **The last button is always export** — copy-as-JSON, copy-as-markdown, copy-as-prompt. Make this prominent.
- Pre-seed with the user's best-guess starting state. Don't make them start from an empty editor.
- Don't add "save / undo / settings" buttons. This is a one-shot editor.

### Example prompt

> I need to reprioritize these 30 Linear tickets. Make me an HTML file with each ticket as a draggable card across Now / Next / Later / Cut columns. Pre-sort them by your best guess. Add a "copy as markdown" button that exports the final ordering with a one-line rationale per bucket.

---

## Pattern: Status report

### Sections

1. Masthead with the period (mono: "Week of 2026-05-12").
2. **Shipped** — list of completed items as a `.row-list` with `.badge success`.
3. **In flight** — same, with `.badge warning`.
4. **Blocked / at risk** — `.card`s with `.risk-tag` and a brief mitigation note.
5. **Next week** — short bulleted list inside a `.callout`.
6. **Bar chart (optional)** — items shipped per week trend.

### Components

- masthead, row-list, badge, risk-tag, callout, optional bar-chart SVG.

### Rules

- Lead with shipped. Buried-lede status reports are a known failure mode.
- Don't include vanity metrics. If you don't have real numbers, omit.

---

## Pattern: Incident timeline

### Sections

1. Masthead with severity badge in red and the duration in mono.
2. **TL;DR callout** in `.danger` — what happened, who was paged, when it resolved.
3. **Minute-by-minute timeline** — `.timeline` with dots colored by phase (detection, escalation, mitigation, resolution).
4. **Log excerpts** — `<pre class="code">` blocks for the critical loglines.
5. **Root cause** — prose section.
6. **Follow-up actions** — `.row-list` with checkbox UI (visual only — no JS needed) and owners.

### Components

- masthead, callout (danger), timeline, code block, row-list.

### Rules

- Times in the timeline are mono UTC timestamps.
- Don't editorialize in the timeline — just events with one-line descriptions.

---

## Pattern: Slide deck

### Sections

A grid of full-viewport slides, navigated with arrow keys.

```css
.slide {
  width: 100vw;
  height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 0 8vw;
  scroll-snap-align: start;
}
.deck { scroll-snap-type: y mandatory; overflow-y: scroll; }
```

### Rules

- One idea per slide. If a slide has more than 30 words, split it.
- Use serif headlines big — h1 size on each slide (use `clamp(40px, 6vw, 88px)`).
- Always have a slide number in mono at the bottom-right corner.
- Add arrow-key navigation in JS: `keydown` → scroll to next/previous slide.

### Example prompt

> Turn this engineering retro into a 5-slide deck: one slide per top-line, big serif headlines, arrow-key navigation.

---

## Don't reach for these defaults if the use case is different

| Tempting default | Skip it for |
|---|---|
| Sticky topbar with nav | Plans, specs, reports, editors — they don't need it |
| Hero banner with gradient | Anything in this aesthetic |
| Three-column features grid | A status report or a code review |
| Generic kanban | An exploration (use the compare grid instead) |
| Wide footer with three columns | Any artifact (use a one-line mono footer) |
