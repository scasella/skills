# Inline SVG diagrams

Diagrams in this aesthetic are **always hand-authored inline SVG**. No Mermaid, no Chart.js, no img tags pointing at external services. The reason: inline SVG inherits the page palette via CSS variables, scales responsively, and is fully editable by the user without round-tripping through a renderer.

## Universal patterns

Every diagram follows these rules:

```svg
<svg viewBox="0 0 600 400" style="width:100%; height:auto; display:block;">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="#87867F"/>
    </marker>
  </defs>
  <!-- nodes and edges -->
</svg>
```

- **`viewBox` always set.** Width 100%, height auto so the diagram scales.
- **Stroke widths:** `1.5` for default borders, `2` for emphasized lines, `2.5` for hand-drawn feel. Never `1` (too thin) or `3+` (too heavy).
- **Colors from the palette.** Use the CSS variables as hex literals inside SVG: `stroke="#87867F"` (g500), `fill="#FFFFFF"` (paper), `stroke="#D97757"` (clay for emphasis).
- **Tinted fills.** Semantic surfaces inside SVG use rgba: `fill="rgba(120,140,93,0.12)"` for olive-tinted nodes.
- **SVG text uses `--mono`**, 10–12px, fill `#141413` (slate) for labels, `#87867F` for sub-labels.
- **Dashed lines** for "no" / "fail" / "future" paths: `stroke-dasharray="4 4"`.
- **Three arrow markers** defined (neutral / olive / rust) so edges can be semantically colored.

```svg
<defs>
  <marker id="arrow"     viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#87867F"/></marker>
  <marker id="arrow-ok"  viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#788C5D"/></marker>
  <marker id="arrow-bad" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#B04A3F"/></marker>
</defs>
```

---

## Flowchart

The most common diagram. Boxes connected by arrows; semantic coloring for success/failure paths.

```svg
<svg viewBox="0 0 620 480" style="width:100%; height:auto;">
  <defs><!-- arrow markers from above --></defs>

  <!-- node: rounded rect + label -->
  <g>
    <rect x="220" y="20"  width="180" height="44" rx="8"
          fill="#FFFFFF" stroke="#141413" stroke-width="1.5"/>
    <text x="310" y="47"  text-anchor="middle"
          font-family="ui-monospace, Menlo, monospace" font-size="12" fill="#141413">
      request arrives
    </text>
  </g>

  <!-- decision node (diamond) -->
  <g>
    <polygon points="310,120 410,180 310,240 210,180"
             fill="rgba(217,119,87,0.12)" stroke="#D97757" stroke-width="1.5"/>
    <text x="310" y="178" text-anchor="middle"
          font-family="ui-monospace, Menlo, monospace" font-size="12" fill="#141413">
      tokens left?
    </text>
    <text x="310" y="194" text-anchor="middle"
          font-family="ui-monospace, Menlo, monospace" font-size="10" fill="#87867F">
      bucket.tokens &gt;= cost
    </text>
  </g>

  <!-- success terminal -->
  <g>
    <rect x="80" y="300" width="180" height="44" rx="8"
          fill="rgba(120,140,93,0.12)" stroke="#788C5D" stroke-width="1.5"/>
    <text x="170" y="327" text-anchor="middle"
          font-family="ui-monospace, Menlo, monospace" font-size="12" fill="#141413">
      forward request
    </text>
  </g>

  <!-- failure terminal -->
  <g>
    <rect x="360" y="300" width="180" height="44" rx="8"
          fill="rgba(176,74,63,0.12)" stroke="#B04A3F" stroke-width="1.5"/>
    <text x="450" y="327" text-anchor="middle"
          font-family="ui-monospace, Menlo, monospace" font-size="12" fill="#141413">
      429 throttle
    </text>
  </g>

  <!-- edges -->
  <path d="M310,64  L310,118" stroke="#87867F" stroke-width="1.5" fill="none" marker-end="url(#arrow)"/>
  <path d="M255,210 L170,298" stroke="#788C5D" stroke-width="1.5" fill="none" marker-end="url(#arrow-ok)"/>
  <path d="M365,210 L450,298" stroke="#B04A3F" stroke-width="1.5" fill="none" marker-end="url(#arrow-bad)" stroke-dasharray="4 4"/>

  <!-- edge labels -->
  <text x="190" y="248" font-family="ui-monospace, Menlo, monospace" font-size="10" fill="#788C5D">yes</text>
  <text x="420" y="248" font-family="ui-monospace, Menlo, monospace" font-size="10" fill="#B04A3F">no</text>
</svg>
```

---

## Bar chart

Inline `<rect>`s. No charting library. Bars + labels + a baseline.

```svg
<svg viewBox="0 0 600 220" style="width:100%; height:auto;">
  <!-- baseline -->
  <line x1="40" y1="180" x2="580" y2="180" stroke="#D1CFC5" stroke-width="1.5"/>

  <!-- bars -->
  <g font-family="ui-monospace, Menlo, monospace" font-size="11" fill="#141413">
    <!-- bar 1 -->
    <rect x="80"  y="80"  width="60" height="100" fill="rgba(217,119,87,0.85)" rx="2"/>
    <text x="110" y="200" text-anchor="middle" fill="#87867F">mon</text>
    <text x="110" y="72"  text-anchor="middle">1.2k</text>

    <!-- bar 2 -->
    <rect x="170" y="40"  width="60" height="140" fill="rgba(217,119,87,0.85)" rx="2"/>
    <text x="200" y="200" text-anchor="middle" fill="#87867F">tue</text>
    <text x="200" y="32"  text-anchor="middle">1.8k</text>

    <!-- bar 3 -->
    <rect x="260" y="100" width="60" height="80"  fill="rgba(217,119,87,0.85)" rx="2"/>
    <text x="290" y="200" text-anchor="middle" fill="#87867F">wed</text>
    <text x="290" y="92"  text-anchor="middle">920</text>

    <!-- bar 4 (highlight) -->
    <rect x="350" y="20"  width="60" height="160" fill="#D97757" rx="2"/>
    <text x="380" y="200" text-anchor="middle" fill="#87867F">thu</text>
    <text x="380" y="12"  text-anchor="middle" fill="#D97757" font-weight="500">2.1k</text>
  </g>
</svg>
```

---

## Line trajectory (for time-series, training curves, etc.)

```svg
<svg viewBox="0 0 600 240" style="width:100%; height:auto;">
  <!-- axes -->
  <line x1="50" y1="20"  x2="50"  y2="200" stroke="#D1CFC5" stroke-width="1.5"/>
  <line x1="50" y1="200" x2="580" y2="200" stroke="#D1CFC5" stroke-width="1.5"/>

  <!-- gridlines (subtle) -->
  <g stroke="#F0EEE6" stroke-width="1">
    <line x1="50" y1="60"  x2="580" y2="60"/>
    <line x1="50" y1="110" x2="580" y2="110"/>
    <line x1="50" y1="160" x2="580" y2="160"/>
  </g>

  <!-- the line itself -->
  <polyline fill="none" stroke="#D97757" stroke-width="2"
            stroke-linecap="round" stroke-linejoin="round"
            points="50,180 130,150 210,140 290,90 370,70 450,55 530,40"/>

  <!-- end-of-line dot -->
  <circle cx="530" cy="40" r="4" fill="#D97757"/>

  <!-- axis labels -->
  <g font-family="ui-monospace, Menlo, monospace" font-size="10" fill="#87867F">
    <text x="50"  y="220" text-anchor="middle">step 0</text>
    <text x="290" y="220" text-anchor="middle">step 5k</text>
    <text x="530" y="220" text-anchor="middle">step 10k</text>
    <text x="40"  y="204" text-anchor="end">0</text>
    <text x="40"  y="164" text-anchor="end">25</text>
    <text x="40"  y="114" text-anchor="end">50</text>
    <text x="40"  y="64"  text-anchor="end">75</text>
    <text x="40"  y="24"  text-anchor="end">100</text>
  </g>
</svg>
```

---

## Architecture / boxes-and-arrows

Service map style. Boxes are tinted by role (api, db, cache, queue). Arrows show data flow.

```svg
<svg viewBox="0 0 720 320" style="width:100%; height:auto;">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#87867F"/></marker>
  </defs>

  <!-- web -->
  <g>
    <rect x="40" y="120" width="140" height="80" rx="10"
          fill="rgba(92,124,163,0.10)" stroke="#5C7CA3" stroke-width="1.5"/>
    <text x="110" y="148" text-anchor="middle"
          font-family="ui-serif, Georgia, serif" font-size="14" fill="#141413">web</text>
    <text x="110" y="170" text-anchor="middle"
          font-family="ui-monospace, Menlo, monospace" font-size="10" fill="#87867F">nginx · 3 pods</text>
  </g>

  <!-- api -->
  <g>
    <rect x="280" y="120" width="140" height="80" rx="10"
          fill="rgba(217,119,87,0.10)" stroke="#D97757" stroke-width="1.5"/>
    <text x="350" y="148" text-anchor="middle"
          font-family="ui-serif, Georgia, serif" font-size="14" fill="#141413">api</text>
    <text x="350" y="170" text-anchor="middle"
          font-family="ui-monospace, Menlo, monospace" font-size="10" fill="#87867F">rails · 12 pods</text>
  </g>

  <!-- db -->
  <g>
    <rect x="520" y="40"  width="160" height="70" rx="10"
          fill="rgba(120,140,93,0.10)" stroke="#788C5D" stroke-width="1.5"/>
    <text x="600" y="68"  text-anchor="middle"
          font-family="ui-serif, Georgia, serif" font-size="14" fill="#141413">postgres</text>
    <text x="600" y="90"  text-anchor="middle"
          font-family="ui-monospace, Menlo, monospace" font-size="10" fill="#87867F">primary + 2 replicas</text>
  </g>

  <!-- cache -->
  <g>
    <rect x="520" y="220" width="160" height="70" rx="10"
          fill="rgba(199,142,63,0.10)" stroke="#C78E3F" stroke-width="1.5"/>
    <text x="600" y="248" text-anchor="middle"
          font-family="ui-serif, Georgia, serif" font-size="14" fill="#141413">redis</text>
    <text x="600" y="270" text-anchor="middle"
          font-family="ui-monospace, Menlo, monospace" font-size="10" fill="#87867F">cluster · 6 shards</text>
  </g>

  <!-- edges -->
  <path d="M180,160 L278,160"   stroke="#87867F" stroke-width="1.5" fill="none" marker-end="url(#arrow)"/>
  <path d="M420,140 L518,80"    stroke="#87867F" stroke-width="1.5" fill="none" marker-end="url(#arrow)"/>
  <path d="M420,180 L518,250"   stroke="#87867F" stroke-width="1.5" fill="none" marker-end="url(#arrow)"/>
</svg>
```

---

## Token bucket / state ring

For consistent hashing, token buckets, or any cyclic concept. A ring with markers around it.

```svg
<svg viewBox="0 0 320 320" style="width:100%; height:auto; max-width:320px;">
  <!-- outer ring -->
  <circle cx="160" cy="160" r="120" fill="none" stroke="#D1CFC5" stroke-width="1.5"/>

  <!-- markers (nodes on the ring) -->
  <g>
    <circle cx="160" cy="40"  r="8" fill="#D97757"/>
    <text   x="160" y="20"    text-anchor="middle"
            font-family="ui-monospace, Menlo, monospace" font-size="10" fill="#87867F">node-a</text>

    <circle cx="280" cy="160" r="8" fill="#788C5D"/>
    <text   x="296" y="164"   text-anchor="start"
            font-family="ui-monospace, Menlo, monospace" font-size="10" fill="#87867F">node-b</text>

    <circle cx="160" cy="280" r="8" fill="#5C7CA3"/>
    <text   x="160" y="304"   text-anchor="middle"
            font-family="ui-monospace, Menlo, monospace" font-size="10" fill="#87867F">node-c</text>

    <circle cx="40"  cy="160" r="8" fill="#C78E3F"/>
    <text   x="24"  y="164"   text-anchor="end"
            font-family="ui-monospace, Menlo, monospace" font-size="10" fill="#87867F">node-d</text>
  </g>

  <!-- key being hashed (smaller, hollow) -->
  <circle cx="244" cy="76" r="5" fill="#FAF9F5" stroke="#141413" stroke-width="1.5"/>
  <text   x="252" y="68"
          font-family="ui-monospace, Menlo, monospace" font-size="10" fill="#141413">key</text>
</svg>
```

---

## When NOT to use SVG

- Pure tabular data with no spatial meaning → use a CSS-Grid table, not SVG.
- Long-form prose with one or two pull-quotes → use callouts, not SVG.
- Code → use `<pre>` with syntax classes, not SVG renderings of code.

The SVG cost is editing-time: hand-authored diagrams require you to lay out coordinates manually. If the user is going to want 20+ nodes, consider whether the page truly needs a diagram, or whether the same idea is clearer as a numbered list with a small accompanying summary SVG.

## Sizing rule of thumb

- Inline diagram in a prose flow: `viewBox` aspect ~16:9, `max-width: 600px`.
- Hero diagram (the page's main figure): `viewBox` ~16:10 or square, full container width.
- Thumbnail / icon: 80×80 viewBox, max-width 80–120px.

## Coordinate hygiene

When laying out a flowchart by hand, use a grid: nodes positioned at multiples of 40 (`x=40, 80, 120, ...`). It makes the diagram look intentional instead of arbitrary.
