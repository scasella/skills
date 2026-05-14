# Components

Paste-ready HTML + CSS for the recurring components across the artifact family. Each component has its CSS first, then its HTML usage. Drop them into the `<style>` and `<body>` blocks as needed.

All components assume the design tokens from `design-tokens.md` are in scope (`--ivory`, `--clay`, `--g300`, etc.).

---

## Masthead (page header)

Every artifact opens with this. Eyebrow → serif headline → one-line lead.

```css
header.masthead {
  padding: 64px 0 40px;
  border-bottom: 1.5px solid var(--g300);
  margin-bottom: 40px;
}
.lead {
  font-size: 17px;
  color: var(--g700);
  line-height: 1.55;
  margin: 18px 0 0;
  max-width: 60ch;
}
```

```html
<header class="masthead">
  <div class="eyebrow">Implementation plan · v1</div>
  <h1>Comment threads on <em>task cards</em></h1>
  <p class="lead">Adds inline threaded replies to every task card, persisted in
     the existing <code>comments</code> table. Two-week scope, three risk areas.</p>
</header>
```

---

## Card

The default container. Floats on the ivory background, never nested inside another card.

```css
.card {
  background: var(--paper);
  border: 1.5px solid var(--g300);
  border-radius: 12px;
  padding: 22px 24px;
  transition: transform .15s ease, box-shadow .15s ease, border-color .15s ease;
}
.card:hover {
  /* only if the card is interactive (a link or button) */
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(20,20,19,.10);
  border-color: var(--slate);
}
.card .card-eyebrow {
  font-family: var(--mono);
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--g500);
  margin-bottom: 8px;
}
.card h3 { margin: 0 0 6px; }
.card p  { color: var(--g700); font-size: 14.5px; margin: 0; }
```

```html
<div class="card">
  <div class="card-eyebrow">Risk #2</div>
  <h3>Migration locks the comments table</h3>
  <p>Adding the <code>thread_id</code> column requires a brief write lock.
     Schedule for off-peak; expected 4–7 seconds.</p>
</div>
```

---

## Badge (pill)

Always `border-radius: 999px`. Used for status, severity, tags.

```css
.badge {
  display: inline-flex;
  align-items: center;
  height: 22px;
  padding: 0 10px;
  font-family: var(--mono);
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.03em;
  border-radius: 999px;
  white-space: nowrap;
}
.badge.success { background: rgba(120,140,93,.16); color: var(--olive); }
.badge.danger  { background: rgba(176,74,63,.16);  color: var(--rust); }
.badge.warning { background: rgba(199,142,63,.18); color: var(--amber); }
.badge.info    { background: rgba(92,124,163,.16); color: var(--steel); }
.badge.neutral { background: var(--g100);           color: var(--g700); }
```

```html
<span class="badge success">DONE</span>
<span class="badge warning">BLOCKING</span>
<span class="badge neutral">2-week scope</span>
```

---

## Risk tag (squared, smaller)

For inline metadata (severity, area, owner). Squared corners distinguish it from the pill badge.

```css
.risk-tag {
  display: inline-block;
  font-family: var(--mono);
  font-size: 10.5px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  padding: 3px 8px;
  border-radius: 6px;
}
.risk-tag.high   { background: rgba(176,74,63,.16);  color: var(--rust); }
.risk-tag.med    { background: rgba(199,142,63,.18); color: var(--amber); }
.risk-tag.low    { background: rgba(120,140,93,.16); color: var(--olive); }
```

---

## Callout / TL;DR (left-stripe)

The left-accent stripe is the signature. Use for summaries, warnings, or "read this first" boxes.

```css
.callout {
  background: var(--paper);
  border: 1.5px solid var(--g300);
  border-left: 3px solid var(--clay);
  border-radius: 10px;
  padding: 16px 18px;
  margin: 24px 0;
}
.callout.warning { border-left-color: var(--amber); }
.callout.danger  { border-left-color: var(--rust); }
.callout.success { border-left-color: var(--olive); }
.callout .callout-label {
  font-family: var(--mono);
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--g500);
  margin-bottom: 6px;
}
.callout p { margin: 0; color: var(--g700); }
```

```html
<div class="callout">
  <div class="callout-label">TL;DR</div>
  <p>Two-week scope. Three risks. Migration is the only blocker — everything
     else is reversible.</p>
</div>
```

---

## Prompt box (quote the original ask)

A gray-100 fill that quotes the user's original prompt. Often the first element after the masthead in research/explainer artifacts.

```css
.prompt-box {
  background: var(--g100);
  border-radius: 10px;
  padding: 16px 18px;
  margin: 0 0 32px;
}
.prompt-box .label {
  display: block;
  font-family: var(--mono);
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--g500);
  margin-bottom: 6px;
}
.prompt-box p { margin: 0; color: var(--g700); font-style: italic; }
```

```html
<div class="prompt-box">
  <span class="label">Prompt</span>
  <p>I don't understand how our rate limiter actually works. Read the relevant
     code and produce a single HTML explainer page…</p>
</div>
```

---

## Code block

Inline `<pre>` with a dark slate panel. Mono font, line-height 1.5.

```css
pre.code {
  background: var(--slate);
  color: #E6E3DA;
  border-radius: 10px;
  padding: 14px 16px;
  font-family: var(--mono);
  font-size: 12.5px;
  line-height: 1.55;
  overflow-x: auto;
  margin: 16px 0;
}
pre.code .kw { color: #D9A55F; }   /* keyword */
pre.code .st { color: #A8B991; }   /* string */
pre.code .cm { color: #87867F; }   /* comment */
pre.code .fn { color: #E3DACC; }   /* function name */

code {  /* inline */
  font-family: var(--mono);
  font-size: 0.92em;
  background: var(--g100);
  color: var(--slate);
  padding: 1.5px 5px;
  border-radius: 4px;
}
```

```html
<pre class="code"><span class="cm">// rate-limiter.ts</span>
<span class="kw">function</span> <span class="fn">checkTokens</span>(key, cost) {
  <span class="kw">const</span> bucket = buckets.get(key);
  <span class="kw">if</span> (bucket.tokens &lt; cost) <span class="kw">return</span> <span class="st">"throttle"</span>;
  bucket.tokens -= cost;
}</pre>
```

---

## Diff renderer

Dark slate background. 3-column grid: line number | mark | code. Tinted-rgba row backgrounds for adds/dels.

```css
.diff {
  background: var(--slate);
  border-radius: 8px;
  padding: 8px 0;
  margin: 16px 0;
  overflow-x: auto;
  font-family: var(--mono);
  font-size: 12.5px;
  line-height: 1.55;
}
.diff-row {
  display: grid;
  grid-template-columns: 48px 22px 1fr;
  padding: 0 12px;
  color: #E6E3DA;
  white-space: pre;
}
.diff-row.add { background: rgba(120,140,93,.18); }
.diff-row.del { background: rgba(176,74,63,.18); }
.diff-row .ln   { color: var(--g500); text-align: right; padding-right: 8px; }
.diff-row .mark { color: var(--g500); }
.diff-row.add .mark { color: #A8B991; }
.diff-row.del .mark { color: #D89A8E; }
```

```html
<div class="diff">
  <div class="diff-row">    <span class="ln">42</span><span class="mark"> </span><span>  if (bucket.tokens &lt; cost) {</span></div>
  <div class="diff-row del"><span class="ln">43</span><span class="mark">-</span><span>    return false;</span></div>
  <div class="diff-row add"><span class="ln">43</span><span class="mark">+</span><span>    return { ok: false, retryAfter: bucket.next };</span></div>
  <div class="diff-row">    <span class="ln">44</span><span class="mark"> </span><span>  }</span></div>
</div>
```

---

## Comment bubble (for PR reviews)

Severity-colored left border. Anchor label at the top, comment body below.

```css
.bubble {
  background: var(--paper);
  border: 1.5px solid var(--g300);
  border-left-width: 4px;
  border-radius: 10px;
  padding: 12px 14px;
  margin: 12px 0;
}
.bubble.blocking { border-left-color: var(--rust); }
.bubble.suggest  { border-left-color: var(--amber); }
.bubble.nit      { border-left-color: var(--steel); }
.bubble .anchor {
  font-family: var(--mono);
  font-size: 11px;
  color: var(--g500);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  margin-bottom: 4px;
}
.bubble p { margin: 0; font-size: 14px; color: var(--g700); }
.bubble .label {
  font-family: var(--mono);
  font-size: 10.5px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  margin-right: 8px;
}
.bubble.blocking .label { color: var(--rust); }
.bubble.suggest .label  { color: var(--amber); }
.bubble.nit .label      { color: var(--steel); }
```

```html
<div class="bubble blocking">
  <div class="anchor">rate-limiter.ts · line 43</div>
  <p><span class="label">Blocking</span>Caller can't recover from a bare
     <code>false</code>. Return the retry-after timestamp so the queue can
     reschedule instead of dropping the job.</p>
</div>
```

---

## Timeline / milestone

3-column grid: when | dot+line | body. The dot column is what makes it feel like a timeline rather than a list.

```css
.timeline { display: grid; gap: 0; margin: 24px 0; }
.milestone {
  display: grid;
  grid-template-columns: 96px 20px 1fr;
  gap: 16px;
  padding: 14px 0;
}
.milestone .when {
  font-family: var(--mono);
  font-size: 12px;
  color: var(--g500);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  padding-top: 2px;
}
.milestone .dot-col {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.milestone .dot {
  width: 10px; height: 10px;
  border-radius: 50%;
  background: var(--clay);
  margin-top: 6px;
}
.milestone .dot.done    { background: var(--olive); }
.milestone .dot.pending { background: var(--paper); border: 1.5px solid var(--g300); }
.milestone .line {
  flex: 1;
  width: 1.5px;
  background: var(--g300);
  margin: 4px 0;
}
.milestone .body h3 { margin: 0 0 4px; }
.milestone .body p  { margin: 0; font-size: 14px; color: var(--g700); }
```

```html
<div class="timeline">
  <div class="milestone">
    <div class="when">Week 1</div>
    <div class="dot-col"><div class="dot done"></div><div class="line"></div></div>
    <div class="body">
      <h3>Schema migration</h3>
      <p>Add <code>thread_id</code> column. Backfill via background job.</p>
    </div>
  </div>
  <div class="milestone">
    <div class="when">Week 2</div>
    <div class="dot-col"><div class="dot"></div></div>
    <div class="body">
      <h3>UI wire-up</h3>
      <p>Reuse the existing <code>CommentList</code> with a new prop.</p>
    </div>
  </div>
</div>
```

---

## Collapsible (`<details>`)

Native `<details>` with a custom rotating arrow. No JS needed.

```css
details {
  border: 1.5px solid var(--g300);
  border-radius: 10px;
  padding: 14px 16px;
  background: var(--paper);
  margin: 12px 0;
}
details summary {
  cursor: pointer;
  list-style: none;
  display: flex;
  align-items: center;
  gap: 10px;
  font-family: var(--serif);
  font-size: 16px;
  color: var(--slate);
}
details summary::-webkit-details-marker { display: none; }
details summary::before {
  content: "▸";
  color: var(--clay);
  font-size: 11px;
  transition: transform .15s ease;
  display: inline-block;
}
details[open] summary::before { transform: rotate(90deg); }
details > *:not(summary) { margin-top: 12px; }
```

```html
<details>
  <summary>Why we picked a thread_id over a parent_id pointer</summary>
  <p>Threads in our product never nest more than one level deep, so a flat
     <code>thread_id</code> is cheaper to query than a recursive CTE…</p>
</details>
```

---

## TOC sidebar (sticky, for explainers)

```css
.layout { display: grid; grid-template-columns: 200px minmax(0, 1fr); gap: 56px; }
.toc {
  position: sticky;
  top: 32px;
  align-self: start;
  border-left: 2px solid var(--g300);
  padding-left: 14px;
}
.toc a {
  display: block;
  font-family: var(--mono);
  font-size: 12px;
  color: var(--g500);
  text-decoration: none;
  padding: 4px 0;
  letter-spacing: 0.02em;
}
.toc a:hover, .toc a.active { color: var(--clay); }
@media (max-width: 920px) { .layout { grid-template-columns: 1fr; } .toc { display: none; } }
```

```html
<div class="layout">
  <nav class="toc">
    <a href="#tldr">TL;DR</a>
    <a href="#flow">Token-bucket flow</a>
    <a href="#code">Key code paths</a>
    <a href="#gotchas">Gotchas</a>
  </nav>
  <main>
    <section id="tldr">…</section>
    <section id="flow">…</section>
  </main>
</div>
```

---

## Avatar (initials in oat circle)

Never images. Initials in a tan circle.

```css
.avatar {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px; height: 28px;
  border-radius: 50%;
  background: var(--oat);
  color: var(--slate);
  font-family: var(--serif);
  font-weight: 500;
  font-size: 12px;
}
```

```html
<span class="avatar">TS</span>
```

---

## Button (primary, secondary)

```css
.btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 14px;
  border-radius: 8px;
  font-family: var(--sans);
  font-size: 13.5px;
  font-weight: 500;
  border: 1.5px solid var(--g300);
  background: var(--paper);
  color: var(--slate);
  cursor: pointer;
  transition: all .12s ease;
}
.btn:hover { border-color: var(--slate); transform: translateY(-1px); }

.btn.primary {
  background: var(--clay);
  border-color: var(--clay);
  color: #fff;
}
.btn.primary:hover { background: var(--clay-d); border-color: var(--clay-d); }

.btn .copied { color: var(--olive); }
```

```html
<button class="btn primary" id="copy">Copy as JSON</button>
<span class="copied" id="copied-msg" hidden>Copied ✓</span>
```

---

## Tables (CSS-Grid style, not <table> with stripes)

```css
.row-list { display: flex; flex-direction: column; }
.row {
  display: grid;
  grid-template-columns: 1fr auto auto auto;
  align-items: center;
  gap: 16px;
  padding: 14px 4px;
  border-bottom: 1px solid var(--g100);
  font-size: 14px;
}
.row:last-child { border-bottom: none; }
.row .meta { font-family: var(--mono); font-size: 12px; color: var(--g500); }
```

```html
<div class="row-list">
  <div class="row">
    <span>Migration: add thread_id column</span>
    <span class="meta">~5s</span>
    <span class="risk-tag med">medium</span>
    <span class="badge success">done</span>
  </div>
  <div class="row">
    <span>UI: thread expand-on-click</span>
    <span class="meta">2d</span>
    <span class="risk-tag low">low</span>
    <span class="badge neutral">in flight</span>
  </div>
</div>
```

---

## Side-by-side comparison grid

For "show me N options" prompts. Each column is one option, labeled with its tradeoff.

```css
.compare {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
  margin: 24px 0;
}
.option {
  background: var(--paper);
  border: 1.5px solid var(--g300);
  border-radius: 12px;
  padding: 20px 22px;
}
.option .tradeoff {
  font-family: var(--mono);
  font-size: 11px;
  color: var(--clay);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-bottom: 8px;
}
.option h3 { margin: 0 0 8px; }
```

```html
<div class="compare">
  <div class="option">
    <div class="tradeoff">Optimizes for speed</div>
    <h3>Two-table join</h3>
    <p>Keep comments and threads separate. One extra query per page render.</p>
  </div>
  <div class="option">
    <div class="tradeoff">Optimizes for simplicity</div>
    <h3>Single denormalized table</h3>
    <p>Push thread_id into the comments table. No joins.</p>
  </div>
</div>
```

---

## Putting components together

The default page composition order:

1. `<header class="masthead">` (eyebrow + h1 + lead)
2. `.prompt-box` (if quoting the user's ask) **or** `.callout` (TL;DR)
3. `<section>` blocks, each with a serif h2 and content built from the components above
4. `<footer>` with timestamps in mono (`Generated 2026-05-13 · v1.0`)

Pick 3–5 of the above components per artifact. Using all of them is a bad sign — it means the page lacks editorial discipline.
