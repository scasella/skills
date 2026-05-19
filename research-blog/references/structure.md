# Article structure

Section progression for a research-experiment writeup. Read this once at the start of drafting to pick which sections you need; not every article uses all of them.

## Default progression

The full progression for a substantial experiment writeup with a follow-up:

```
Hero
  H1 title
  subtitle (one sentence framing what the article covers)
  date / byline (sans, uppercase)
  paper-links (Github, Recipe, Paper — pill buttons)

Body (single 720px column, body-main wrapper)
  TL;DR                    [.tldr — pulled-quote]
  H2: The question         [callout with one-sentence question]
  H2: Setup                [3 H3 sub-sections + stat-row]
  H2: Method               [mode-grid 2x2]
  H2: The headline         [stat-row + Table 01]
    H3: One detail         [supporting paragraph]
    [callout: sanity check]
  H2: Mechanism check      [chart + Table 02 with replication signature]
  H2: Bounds on the claim  [callout listing what's not claimed]
  H2: [Followup section]   [chart + tables specific to the followup]
    [.neg-list — honest scope]
  H2: What's next          [3-4 H3 sub-sections, each one short paragraph]
  break (· · ·)
  Closing two paragraphs   [restate what holds, what's open]

Footer (dark)
  subscribe form
  footer-meta with author / setup / data links
```

## Section templates

### TL;DR
Two paragraphs max. Pulled-quote treatment with left rule.

```html
<div class="tldr">
  <span class="tldr-label">TL;DR</span>
  <p>
    [Sentence 1: setup framing — what was compared, on what backbone.]
    [Sentence 2: the headline finding with key numbers, statistical context, and what was held constant.]
    [Sentence 3: the mechanism in one clause.]
  </p>
  <p>
    [Optional second paragraph for follow-up findings or update notes — opens with "Update — [date]." in bold.]
  </p>
</div>
```

Anti-pattern: leading with "We did X. We found Y. We conclude Z." — too autobiographical. Lead with the comparison structure or the result framing instead.

### The question
Open with the broader context (what's the field default?), then narrow to the specific question this article answers. Use a callout to hold the question itself.

```html
<h2 id="question">[The question we couldn't skip / The question we asked / similar]</h2>

<p>[Paragraph: what's the default? What's invisible about it?]</p>
<p>[Paragraph: what alternative did we try? Why now?]</p>

<div class="callout">
  <span class="callout-label">The question</span>
  <p>[One-sentence question, ideally with a binary frame.]</p>
</div>

<p>[Paragraph: the answer, in one or two sentences. Don't over-elaborate; the rest of the article unpacks it.]</p>
```

### Setup — one backbone, two scaffolds
3 H3 sub-sections (backbone, model under test, baseline) + a callout naming what was held constant + a stat-row of compute/budget context.

```html
<h2 id="setup">Setup — [framing]</h2>

<p>[One-sentence framing of why setup matters more than result here.]</p>

<h3>The backbone</h3>
<p>[Model name, parameter count, architecture quirks, available variants.]</p>

<h3>The model under test</h3>
<p>[Recipe in compressed form: starting point, training stages, hyperparameters, total step count. End with "That is the entire recipe."]</p>

<pre><code>[code template / prompt template if relevant]</code></pre>

<h3>The baseline</h3>
<p>[What is the comparison? Why is it the cleanest available peer?]</p>

<div class="callout">
  <span class="callout-label">What makes this comparison fair</span>
  <p>[List of axes held constant; name the axes that vary.]</p>
</div>

<div class="stat-row">[4 tiles of compute / training budget context]</div>
```

### Method
Use the mode-grid 2×2 for procedural steps. Each card has a tag (`01 · extract`, `02 · embed`, ...), a title, and a one-line description.

```html
<h2 id="method">Measuring "[the property]"</h2>

<p>[Paragraph: why operationalising this matters; describe the procedure in one paragraph.]</p>

<div class="mode-grid">
  <div class="mode-card">
    <span class="tag">01 · [verb]</span>
    <span class="t">[short title]</span>
    <span class="desc">[one-paragraph description with concrete params]</span>
  </div>
  <!-- 3 more cards -->
</div>

<p>[Paragraph: scope of the analysis (n problems, paired vs unpaired, etc.).]</p>
```

### The headline
Open with mechanism, drop a stat-row, then the canonical comparison table.

```html
<h2 id="result">The headline — [one phrase]</h2>

<p>[Paragraph: explain what the metric measures and why it's a proxy for the underlying claim.]</p>

<div class="stat-row">[4 tiles of headline numbers with statistical context]</div>

<div class="table-wrap">
  <div class="table-label"><span class="id">Table 01</span>[caption]</div>
  <table>...</table>
</div>

<p>[Paragraph: address the obvious confound — does the result hold across difficulty regimes? Lead with the confound, then dispatch it.]</p>

<h3>[A load-bearing detail — e.g. "The lift is not from verbosity"]</h3>
<p>[Paragraph addressing the most likely alternative explanation.]</p>

<div class="callout">
  <span class="callout-label">[Sanity check name]</span>
  <p>[One-paragraph result of an additional check that rules out an artifact.]</p>
</div>
```

### Mechanism check / replication signature
The most important section after the headline. The first chart goes here. The structure is: (1) state what would falsify the claim, (2) show the test, (3) show the replication across slices.

```html
<h2 id="passk">[The X signature — search that compounds / the trajectory / etc.]</h2>

<p>[Paragraph: explain the predicted mechanical consequence — what should happen if the claim is true?]</p>

<figure class="chart">[Chart 1 — the mechanical signature]</figure>

<p>[Optional one-line bridge: "And it's not a one-off."]</p>

<div class="table-wrap">
  <div class="table-label"><span class="id">Table 02</span>[caption — replication across slices]</div>
  <table>...</table>
</div>

<p>[One-sentence closer affirming the mechanism is independent of the primary measurement.]</p>
```

### Bounds on the claim
Always present. The voice depends on it. Use a callout for the negative bounds, a paragraph for the next-step framing.

```html
<h2 id="limits">Bounds on the claim</h2>

<p>[One-line setup.]</p>

<div class="callout">
  <span class="callout-label">What the result is not</span>
  <p>[Paragraph listing what's not claimed — accuracy gap, subset relationship, compromised metrics, etc.]</p>
</div>

<p>[Paragraph naming the most-pressing follow-up question.]</p>
```

### Followup section (optional)
Same structure as a mini-article: question, setup, result, mechanism, scope. Use H3s for sub-sections rather than H2s — keeps the followup nested under the main story.

```html
<h2 id="followup">[Direct title for the followup, e.g. "From X to Y"]</h2>

<p>[Paragraph: how does this build on the headline?]</p>
<p>[Paragraph: the new measurement / experiment.]</p>
<p>[Paragraph: pool / setup details, with code identifiers in monospace.]</p>

<h3>[Sub-result 1 title]</h3>
<p>[Lead sentence with the result.]</p>
<div class="stat-row">[4 tiles]</div>
<p>[Mechanism paragraph.]</p>

<h3>[Sub-result 2 title]</h3>
<p>[Lead sentence.]</p>
<div class="table-wrap">[Contingency table or comparison]</div>
<p>[What this row says.]</p>

<h3>[Trajectory title]</h3>
<p>[One-paragraph setup.]</p>
<figure class="chart">[Chart 2 — followup trajectory]</figure>

<h3>[Mechanism title]</h3>
<p>[Setup.]</p>
<div class="table-wrap">[Per-source / per-condition table]</div>
<p>[Two readings of the table.]</p>

<h3>[Scope title]</h3>

<div class="neg-list">
  <span class="neg-list-label">Honest scope</span>
  <ul>
    <li><strong>Does say:</strong> [...]</li>
    <li><strong>Does not say:</strong> [...]</li>
    <li><strong>[Caveat name]:</strong> [...]</li>
  </ul>
</div>
```

### What's next
2–4 H3 sub-sections, each one short paragraph. Order by which would most sharpen the claim.

```html
<h2 id="next">What's next</h2>

<p>[One paragraph: what was closed by this article, what's still open.]</p>

<h3>[Item 1 title — the highest-value next experiment]</h3>
<p>[Paragraph: what to run, wall-time / compute estimate, what it decides.]</p>

<h3>[Item 2]</h3>
<p>[Paragraph.]</p>

<h3>[Item 3]</h3>
<p>[Paragraph.]</p>

<h3>[Item 4]</h3>
<p>[Paragraph.]</p>

<div class="break">· · ·</div>

<p>[Closing paragraph 1: restate the headline, now with the followup integrated.]</p>
<p>[Closing paragraph 2: name the remaining questions specifically; gesture at the further-out question without claiming it.]</p>
```

## Sections to skip when

- **No followup yet** → drop the followup section. Default is fine without it.
- **Single-result article** → drop the mechanism/replication-signature section. Limits + What's next still apply.
- **Pure observation, no experiment** → wrong skill. Use a different tool.
- **Methods paper** → keep Setup but expand it; replace Method with a longer procedural section. Drop the headline-stat-row pattern in favor of method tables.

## ID convention

Use semantic ids on H2s for in-page anchoring even though the template doesn't render a TOC by default. Standard ids:

`question`, `setup`, `method`, `result`, `passk` (or whatever the mechanism-check section is called), `limits`, `<followup-slug>`, `next`.

## Length targets

- Total article: 1,500–4,000 words. The diversity-effect prototype is ~5,800 words and reads as long; aim shorter for first drafts.
- TL;DR: 80–150 words across both paragraphs.
- Each H2 section: 200–800 words. If a section is over 1,000 words, split it.
- Each H3 sub-section: 60–250 words.
- Closing two paragraphs: 100–250 words combined.
