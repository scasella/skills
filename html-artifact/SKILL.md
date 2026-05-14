---
name: html-artifact
description: Outputs deliverables as polished single-file HTML pages instead of markdown — the warm-cream-and-clay aesthetic of Thariq Shihipar's "Unreasonable Effectiveness of HTML". Use this whenever the user asks for any artifact, plan, spec, report, writeup, code review, PR explainer, brainstorm, design exploration, mockup, prototype, sandbox, status update, post-mortem, slide deck, or custom editor — even when they say "markdown", "document", "doc", "file", "writeup", or don't specify a format at all. Once content gets richer than a hundred lines or needs diagrams, diffs, color, tables, or interactivity, markdown stops paying its way; this skill replaces it with information-dense HTML featuring serif headlines, mono meta labels, inline SVG diagrams, tinted callouts, and (where useful) interactive controls with copy-back-to-prompt buttons. Triggers on phrases like "make a plan", "write up", "spec out", "review this PR", "explain how X works", "create a report", "design an onboarding screen", "prototype an animation", "build me an editor for", "summarize this", "give me a writeup", "make me a doc", and similar deliverable requests — prefer HTML over markdown even when not asked explicitly.
---

# HTML artifact

The default output format for anything richer than a chat reply. Replaces markdown for plans, specs, code reviews, research explainers, design explorations, custom editors, and reports.

## Why HTML over markdown

Markdown is fine for short replies and quickly-edited notes. It stops paying its way once the document needs any of:

- color, diagrams, tables more than a few rows
- spec/plan content longer than ~100 lines (people stop reading)
- diffs, annotated code, flowcharts, timelines
- interactive controls (sliders, drag-and-drop, copy-back-to-prompt buttons)
- a shareable link instead of an email attachment

For those, output a single self-contained `.html` file. The user opens it in a browser, can share it via S3/static host, and — crucially — is far more likely to actually read it.

The user wants to feel in the loop with what you're producing. A well-built HTML page invites them in; a 600-line markdown plan makes them rubber-stamp. Optimize for "they actually read it and push back on the right parts."

## When this skill fires

**Always-prefer-HTML triggers** (output HTML even if the user said "markdown" or didn't specify):

- "make a plan / spec / writeup / doc / report / summary / explainer"
- "review this PR / explain this PR / write up this PR"
- "brainstorm / explore options / show me approaches / compare designs"
- "explain how X works / how does our X work / I don't understand X"
- "weekly status / incident report / post-mortem / retro"
- "prototype / mockup / sandbox / playground / design system"
- "build me an editor / triage tool / configurator for X"
- "diagram / flowchart / illustrate / visualize"

**Stay-in-markdown exceptions** (don't fire):

- The user is asking a quick question with a short text answer.
- The output is meant to be ingested by another tool that expects markdown (CLAUDE.md, README the user explicitly named as `.md`, GitHub issue body, commit message).
- The user explicitly says "in markdown please" or "no html" — respect it.

When in doubt, default to HTML. Markdown is the constraining choice; this skill exists to break the markdown habit.

## Reading order — DO THIS FIRST

Before writing any HTML, read in this order:

1. **`references/use-cases.md`** — pick the right skeleton for the prompt (spec / code review / explainer / design exploration / editor / report). Each use case has its own layout pattern; using the wrong skeleton is the #1 way to produce generic-feeling output.
2. **`references/design-tokens.md`** — the CSS variables, type stacks, and spacing scale. Paste this verbatim into `<style>`; do not reinvent it.
3. **`references/components.md`** — pick the components your page needs (eyebrow, card, badge, callout, diff, timeline, prompt-box, etc.) and paste them in.
4. **`references/svg-diagrams.md`** — if your page has any kind of diagram (flow, ring, comparison, bar chart), copy the relevant SVG skeleton instead of trying to write SVG from scratch.
5. **`references/interactivity.md`** — only if the user wants something interactive (drag-and-drop, sliders, copy-to-clipboard, live preview, tabs).

`assets/starter.html` is a paste-and-extend boilerplate already wired up with the palette, eyebrow, masthead, and one example card. Start from it for short artifacts; for long ones, use it as the skeleton and add sections.

## Core principles (the look)

These are not stylistic preferences — they are what distinguishes this aesthetic from generic AI-generated HTML. Hold the line on all of them:

1. **One self-contained `.html` file.** Inline `<style>` and `<script>`. No build step, no external CSS, no Tailwind, no React, no Google Fonts, no CDN imports. The user opens the file directly in a browser. If you find yourself reaching for `<link rel="stylesheet">` or `<script src="https://">`, stop.

2. **System font stacks only — three of them, with rigid roles.**
   - `--serif` (`ui-serif, Georgia, ...`) for every heading (h1/h2/h3), at `font-weight: 500`. Headings are *display* typography, not bold.
   - `--mono` (`ui-monospace, "SF Mono", Menlo, ...`) for every "meta" element: eyebrows, file paths, line numbers, badges, hex codes, timestamps, code. Uppercase eyebrows with `letter-spacing: 0.08–0.12em`.
   - `--sans` (`system-ui, -apple-system, ...`) for body text only.

3. **Warm cream page (`#FAF9F5`) under white cards.** Never a pure-white page background. Never dark mode unless the user asks.

4. **Clay (`#D97757`) is the ONE accent.** Used sparingly — links, primary buttons, italic emphasis inside serif headings, eyebrow ticks. Not as a hero gradient. Not as a card fill.

5. **1.5px borders everywhere.** Not 1px, not 2px. It is the single most identifying visual detail.

6. **Tinted-rgba semantic surfaces.** Success / warning / danger backgrounds are 10–16% alpha of the semantic color (olive / amber / rust), never solid green/red/yellow.

7. **Inline SVG for every diagram.** No Mermaid, no Chart.js, no img tags pointing at external images. SVG `viewBox` always set, `width: 100%; height: auto` so the diagram is responsive.

8. **Vanilla JS only.** One bottom `<script>` block, IIFE-wrapped. No imports, no JSX, no React. ES5-ish (`var`, `function`, `forEach`) for legibility.

9. **Custom editors export.** If the page is an editor (triage board, flag editor, prompt tuner), the last button is always **copy-as-JSON / copy-as-markdown / copy-as-prompt** so the user can paste the result back into Claude. The editor is a one-way data round-trip, not a SaaS product.

10. **Mobile responsive with one breakpoint.** Desktop-first; collapse grids to single column at `@media (max-width: 880px)` (or 640/920 depending on layout). Hide the TOC sidebar on mobile.

## Anti-patterns — what NEVER to do

If the output drifts toward any of these, you've fallen back into generic-AI-HTML mode. Stop and rewrite.

- **No Tailwind utility soup.** Hand-written semantic class names only.
- **No purple-to-pink gradients, no glassmorphism, no neumorphism, no backdrop blur.**
- **No `border-radius` over 14px on cards.** Pills are 999px; cards/rows are 8–14px.
- **No `font-weight: 700` on headings.** Bold is reserved for inline `<b>` and badges.
- **No imported Google fonts** (Inter, Geist, JetBrains Mono). System stacks only.
- **No SaaS hero pattern** (centered giant gradient h1 + two CTAs). Headers are left-aligned: eyebrow → serif title → one-line lead.
- **No emoji clutter.** A single `✓` after "Copied" is acceptable. Avoid otherwise.
- **No icon libraries** (Lucide, Heroicons, Font Awesome). Tiny inline SVG paths or unicode (`▸`, `→`).
- **No `<canvas>` or charting libs.** Bar charts are inline `<rect>`s.
- **No box around the whole page.** The cream background carries it; cards float on it.
- **No drop shadows except `0 10px 30px rgba(20,20,19,.10)` on card hover.**
- **No tables with zebra stripes.** Use CSS Grid rows with `border-bottom: 1px solid var(--g100)`.

If the user critiques the output as "looks like AI made it", the fix is almost always: pull `border-radius` down, swap any non-system font for system stacks, remove drop shadows, replace solid semantic colors with tinted-rgba, and rebalance the typography toward serif-display + mono-meta + sans-body.

## Workflow

1. **Read the use-case playbook.** `references/use-cases.md` — pick the skeleton.
2. **Open `assets/starter.html`** and copy it as your starting point. The palette, masthead, and one example card are already wired up.
3. **Add the sections the use case calls for.** Pull components from `references/components.md`, diagrams from `references/svg-diagrams.md`.
4. **For an editor / sandbox**: add the script block, modeled on `references/interactivity.md`. Always end with a copy-to-clipboard button.
5. **Save with a descriptive filename**: `<topic>-<kind>.html` (e.g., `rate-limiter-explainer.html`, `q4-feature-flags-editor.html`). Lowercase, hyphens, no spaces. Save to the working directory unless the user specified a path.
6. **Open it in the browser** with `open <file>.html` (macOS) so the user can immediately see it. Mention the filename in your response.
7. **Don't ask follow-up questions before generating.** Make reasonable defaults and ship. The user iterates by responding; that's the loop.

## Token budget

HTML takes 2–4× the tokens of equivalent markdown. That is the cost; pay it. With the 1M context window, it is rarely a blocker. If you genuinely run into a length problem on a very long artifact, split into multiple linked HTML files rather than degrading to markdown.

## After generating

End your response with a short note like: "Saved as `rate-limiter-explainer.html` and opened in your browser. Tell me what to change." Do not summarize the contents of the document — the user can read it. Do not paste large excerpts of the HTML back into the chat.

## When the user pushes back

- "Make it less busy / quieter" → reduce the number of distinct components on screen, tighten the color palette to ivory + slate + one clay accent (drop olive/rust if they're not load-bearing), drop hover effects on non-interactive elements.
- "It's ugly / looks AI-generated" → re-check the anti-patterns list above. Almost always the culprits are radii, drop shadows, non-system fonts, or solid semantic colors.
- "Use my company's design system" → ask the user to point you at a file or page in their codebase. Create a `design-system.html` reference once, then point future HTML artifacts at it.
- "I want to interact with it" → add a script block per `references/interactivity.md`. End with a copy-back-to-prompt button.

## Examples of the form

The 21 example HTML files at https://thariqs.github.io/html-effectiveness/ are the ground truth for the aesthetic. If the user wants to see the reference style, point them there.
