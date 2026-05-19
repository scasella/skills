---
name: research-blog
description: >-
  Builds a complete self-contained HTML research blog post from experimental
  results. Use when the user wants to publish, write up, share, or turn
  empirical findings into a polished web article. Triggers include blog post,
  writeup, lab writeup, publishable post, research writeup, HTML page about
  findings, and similar requests. Produces a warm editorial single-file HTML
  artifact with embedded SVG charts, stat tiles, restrained forensic voice,
  and explicit caveats. Out of scope: literature reviews, opinion pieces,
  marketing pages, slide decks, and README files.
---

# research-blog

A skill for turning experimental results into a publishable, self-contained HTML blog post in the multi-model lab style — warm cream background, light editorial serif body, minimal monochrome SVG charts, dark footer. Single-file output, no build step, no JS frameworks.

## When to invoke

Trigger when the user has:
- Numbers from an experiment they ran (training curves, pass rates, classification counts, A/B comparisons)
- A claim they want to communicate ("the variance band is 1.83× wider", "RL doubles held-out pass rate")
- A request that implies external publication: "blog post", "write up", "share this", "publishable", "make an HTML page"

Don't invoke for: README files, internal lab notes (use plain markdown), slide decks, marketing copy, opinion essays, literature reviews. The skill assumes there's an experiment with results.

## Workflow

1. **Gather the inputs**. Before drafting, you need:
   - The headline finding (one sentence: what changed, by how much, on what)
   - 2–6 key numbers (with statistical context: stderr, n, p-value, paired-test stat where relevant)
   - The mechanism (why the change happened — the causal story)
   - At least one chartable trajectory or comparison
   - The honest caveats (what wasn't tested, single seed, missing baseline, etc.)

   If any of these are missing, ask the user before drafting. Don't fabricate numbers or invent caveats.

2. **Pick chart types** from `references/chart-patterns.md`:
   - Trajectory over a continuous variable (RL step, k, dataset size) → **line chart**
   - Two arms compared at a few discrete points → **grouped bar chart**
   - 3×3 / 4×4 cross-tabulation → **contingency table** (HTML, not SVG)
   - 4 headline numbers → **stat-tile row**

3. **Choose section structure** from `references/structure.md`. The default progression for an experiment writeup:
   TL;DR → The question / motivation → Setup → Method → Headline result (with first chart) → Mechanism / replication signature (with second chart or table) → Bounds on the claim → Followup section (if applicable) → What's next → Closing two paragraphs.

4. **Write in the voice from `references/voice-profile.md`**. The forensic mentor register — mechanism leads sentences, numbers follow, hedging is via specificity not modal verbs, italics only on defined concepts, em-dashes used sparingly.

5. **Fill the template at `assets/template.html`**. The template is a complete working HTML scaffold with all CSS, the standard header/footer, placeholder slots for every section. Replace placeholders, drop or duplicate sections as needed, embed your charts inline as SVG.

6. **Write to a single self-contained `.html` file**. No external assets beyond the Google Fonts link (which is in the template head). Verify the file works by opening it (or asking the user to).

## Reference files

Read these only as needed — they're loaded out-of-context until you reach for them:

- **`references/design-system.md`** — color tokens, type scale, layout primitives, what every CSS class does. Read when you need to verify a token or extend a component.
- **`references/voice-profile.md`** — writing rules with paired before/after examples. Read before you start writing prose.
- **`references/chart-patterns.md`** — SVG templates for each chart type with the coordinate math worked out. Read when you're about to embed a chart.
- **`references/structure.md`** — section-by-section templates with example openings. Read once at the start of a long article to pick the progression.

## Asset

- **`assets/template.html`** — the canonical scaffold. Copy it to the output path and fill in. Has working CSS, header, hero, every component class, footer. Includes commented placeholders showing where each section goes.

## Output convention

Save to a path the user provides, or default to `reports/blog_post/<slug>.html` relative to the project. The output is one HTML file. Don't generate companion CSS, JS, or assets files — the design assumes single-file portability.

## What to avoid

- **Don't fabricate numbers** to fill the template. If the user hasn't provided a held-out trajectory but you're rendering a line chart, ask for the data instead of inventing it.
- **Don't switch the visual aesthetic.** This skill ships one opinionated style. If the user wants dark mode or a different color palette, surface the constraint rather than silently restyling — the consistency is the point.
- **Don't skip the caveats section.** The voice profile depends on the article including honest scope. A blog post that only reports wins reads as marketing in this template.
- **Don't write a "what we did" autobiographical narrative.** The voice is forensic, not memoir. Lead with mechanism and result, not chronology of the work.

## Iteration

After writing the first draft, the user will usually want to refine prose, swap colors in a chart, restructure a section, or trim the read time. Make targeted edits in place rather than regenerating the whole file. The template is stable; the prose is what iterates.
