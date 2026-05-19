# Chart patterns

Four primitive chart types. Each one has the coordinate math worked out so you can drop in your data, recompute, and embed.

All charts:
- Background fill: `#F9F9F6` (page bg)
- Title: serif 18px weight 400, color `#3B3B39`, centered
- Subtitle: sans 12px, color `#969592`, centered
- Axis labels: sans 11px, color `#969592`
- Data text labels: sans 11px, color `#3B3B39`
- viewBox internal coords scale fluidly to any container width — at desktop the breakout container is ~1200–1320px wide, so a 960×460 viewBox renders at ~1.25–1.4× the SVG's native pixel size

Wrap every chart in:
```html
<figure class="chart">
  <svg viewBox="..." role="img" aria-label="...">...</svg>
  <figcaption><strong>Figure N.</strong> One-paragraph caption describing what's shown, the n, the estimator, and what to read from the trajectory.</figcaption>
</figure>
```

`figure.chart` must be a **direct child of `.body-main`** for the breakout-width rule to apply.

---

## 1. Line trajectory (single series over a continuous variable)

Use for: training curves, pass@k vs k, held-out vs RL step. One metric vs one ordinal x-axis.

**Sage-teal stroke, dotted reference line at the baseline.** Highlights peak/last points with darker accent fill.

Coordinate math (viewBox 960×460):
- Plot area: x ∈ [80, 880], y ∈ [110, 380] (270 px height for full y range)
- y → pixel: `y_px = 380 - value * (270 / y_max)`
- Bars/points x positions: `x_i = 130 + i * step_x` for evenly spaced ticks

Template:
```html
<figure class="chart">
  <svg viewBox="0 0 960 460" role="img" aria-label="[brief description]">
    <rect x="0" y="0" width="960" height="460" fill="#F9F9F6" />

    <!-- title row -->
    <text x="480" y="30" text-anchor="middle" fill="#3B3B39"
          font-family="Libre Baskerville, Georgia, serif" font-size="18" font-weight="400">
      [Chart title]
    </text>
    <text x="480" y="54" text-anchor="middle" fill="#969592"
          font-family="Inter, sans-serif" font-size="12">
      [Chart subtitle — what to read from it]
    </text>

    <!-- legend -->
    <line x1="350" y1="78" x2="382" y2="78" stroke="#5C8A95" stroke-width="2.5" />
    <text x="388" y="82" fill="#3B3B39" font-family="Inter, sans-serif" font-size="12">[series label]</text>
    <line x1="568" y1="78" x2="600" y2="78" stroke="#969592" stroke-width="1.5" stroke-dasharray="4 4" />
    <text x="606" y="82" fill="#3B3B39" font-family="Inter, sans-serif" font-size="12">[reference label]</text>

    <!-- y-axis line + grid -->
    <line x1="80" y1="380" x2="880" y2="380" stroke="#C8C7C2" stroke-width="1" />
    <line x1="80" y1="303" x2="880" y2="303" stroke="#E4E3DE" stroke-width="1" />
    <line x1="80" y1="226" x2="880" y2="226" stroke="#E4E3DE" stroke-width="1" />
    <line x1="80" y1="149" x2="880" y2="149" stroke="#E4E3DE" stroke-width="1" />

    <!-- y-tick labels -->
    <text x="72" y="384" text-anchor="end" fill="#969592" font-family="Inter, sans-serif" font-size="11">0%</text>
    <text x="72" y="307" text-anchor="end" fill="#969592" font-family="Inter, sans-serif" font-size="11">10%</text>
    <text x="72" y="230" text-anchor="end" fill="#969592" font-family="Inter, sans-serif" font-size="11">20%</text>
    <text x="72" y="153" text-anchor="end" fill="#969592" font-family="Inter, sans-serif" font-size="11">30%</text>

    <!-- baseline reference line at y=BASELINE_Y, label inside chart on right -->
    <line x1="80" y1="BASELINE_Y" x2="880" y2="BASELINE_Y" stroke="#969592" stroke-width="1" stroke-dasharray="4 4" opacity="0.7" />
    <text x="876" y="BASELINE_Y_MINUS_4" text-anchor="end" fill="#969592" font-family="Inter, sans-serif" font-size="10">[baseline label]</text>

    <!-- main polyline -->
    <polyline points="X0,Y0 X1,Y1 X2,Y2 ..."
              fill="none" stroke="#5C8A95" stroke-width="2.5"
              stroke-linecap="round" stroke-linejoin="round" />

    <!-- area under curve, very faint -->
    <polygon points="X0,Y0 X1,Y1 ... XN,YN XN,380 X0,380"
             fill="#5C8A95" opacity="0.08" />

    <!-- data points (small circles, peaks use larger dark circle) -->
    <circle cx="X" cy="Y" r="4" fill="#5C8A95" />
    <circle cx="PEAK_X" cy="PEAK_Y" r="5" fill="#3B3B39" />

    <!-- value labels on key points (start, peaks, end) -->
    <text x="X" y="Y_MINUS_6" text-anchor="middle" fill="#3B3B39" font-family="Inter, sans-serif" font-size="11">.290</text>

    <!-- x-axis tick labels -->
    <text x="X" y="402" text-anchor="middle" fill="#3B3B39" font-family="Inter, sans-serif" font-size="11">[tick label]</text>
    <text x="480" y="426" text-anchor="middle" fill="#969592" font-family="Inter, sans-serif" font-size="11">[x-axis title]</text>

    <!-- footer note -->
    <text x="80" y="448" fill="#969592" font-family="Inter, sans-serif" font-size="11">[note: stderr, n, sampling caveat]</text>
  </svg>
  <figcaption>[caption]</figcaption>
</figure>
```

---

## 2. Grouped bar / multi-series line (two arms compared at a few discrete points)

Use for: pass@k panel-vs-thinking at k=1,4,8,16; before/after comparisons across multiple categories.

**Two series. Primary in solid dark stroke, secondary in dashed gray.** When the comparison is "trail-but-converge" (panel vs thinking pass@k), show both as polylines with the gap closing visually.

Coordinate math (viewBox 960×460):
- Plot area: x ∈ [80, 880], y ∈ [110, 380] (270 px height, y_max = 1.0 for pass rates)
- y → pixel: `y_px = 380 - value * 270`
- For 4 x-ticks, position at: 180, 380, 580, 780

Template:
```html
<figure class="chart">
  <svg viewBox="0 0 960 460" role="img" aria-label="[description]">
    <rect x="0" y="0" width="960" height="460" fill="#F9F9F6" />

    <text x="480" y="30" text-anchor="middle" fill="#3B3B39"
          font-family="Libre Baskerville, Georgia, serif" font-size="18" font-weight="400">[title]</text>
    <text x="480" y="54" text-anchor="middle" fill="#969592"
          font-family="Inter, sans-serif" font-size="12">[subtitle]</text>

    <!-- legend -->
    <line x1="370" y1="78" x2="402" y2="78" stroke="#3B3B39" stroke-width="2" />
    <text x="408" y="82" fill="#3B3B39" font-family="Inter, sans-serif" font-size="12">[series A label]</text>
    <line x1="498" y1="78" x2="530" y2="78" stroke="#969592" stroke-width="2" stroke-dasharray="4 3" />
    <text x="536" y="82" fill="#3B3B39" font-family="Inter, sans-serif" font-size="12">[series B label]</text>

    <!-- gridlines + tick labels (0%, 25%, 50%, 75%, 100%) -->
    <line x1="80" y1="380" x2="880" y2="380" stroke="#C8C7C2" stroke-width="1" />
    <line x1="80" y1="312.5" x2="880" y2="312.5" stroke="#E4E3DE" stroke-width="1" />
    <line x1="80" y1="245" x2="880" y2="245" stroke="#E4E3DE" stroke-width="1" />
    <line x1="80" y1="177.5" x2="880" y2="177.5" stroke="#E4E3DE" stroke-width="1" />
    <line x1="80" y1="110" x2="880" y2="110" stroke="#E4E3DE" stroke-width="1" />

    <text x="72" y="384" text-anchor="end" fill="#969592" font-family="Inter, sans-serif" font-size="11">0%</text>
    <text x="72" y="316" text-anchor="end" fill="#969592" font-family="Inter, sans-serif" font-size="11">25%</text>
    <text x="72" y="249" text-anchor="end" fill="#969592" font-family="Inter, sans-serif" font-size="11">50%</text>
    <text x="72" y="181" text-anchor="end" fill="#969592" font-family="Inter, sans-serif" font-size="11">75%</text>
    <text x="72" y="114" text-anchor="end" fill="#969592" font-family="Inter, sans-serif" font-size="11">100%</text>

    <!-- series A: solid dark line + filled circles -->
    <polyline points="180,Y_A1 380,Y_A2 580,Y_A3 780,Y_A4"
              fill="none" stroke="#3B3B39" stroke-width="2.5"
              stroke-linecap="round" stroke-linejoin="round" />
    <circle cx="180" cy="Y_A1" r="4" fill="#3B3B39" />
    <!-- ... more circles -->

    <!-- series B: dashed gray line + open circles -->
    <polyline points="180,Y_B1 380,Y_B2 580,Y_B3 780,Y_B4"
              fill="none" stroke="#969592" stroke-width="2"
              stroke-dasharray="5 4" stroke-linecap="round" stroke-linejoin="round" />
    <circle cx="180" cy="Y_B1" r="3.5" fill="#fff" stroke="#969592" stroke-width="1.5" />
    <!-- ... more open circles -->

    <!-- value labels (primary series only — secondary stays unlabeled) -->
    <text x="180" y="Y_A1_PLUS_18" text-anchor="middle" fill="#3B3B39" font-family="Inter, sans-serif" font-size="11">.225</text>

    <!-- x-axis labels + per-point gap annotations -->
    <text x="180" y="404" text-anchor="middle" fill="#3B3B39" font-family="Inter, sans-serif" font-size="12">[tick]</text>
    <text x="180" y="424" text-anchor="middle" fill="#969592" font-family="Inter, sans-serif" font-size="11">Δ -50.6pp</text>

    <text x="80" y="448" fill="#969592" font-family="Inter, sans-serif" font-size="11">[closure / mechanism note]</text>
  </svg>
  <figcaption>[caption — include the estimator formula if relevant]</figcaption>
</figure>
```

---

## 3. Contingency table (cross-tabulation)

Use for: 3×3 or 4×4 categorical breakdowns where row and column totals matter (joint variance band, confusion matrix, etc.).

**Render as HTML `<table>`, not SVG.** The table component handles tabular-nums alignment, the highlight row, and the totals row.

Template:
```html
<div class="table-wrap">
  <div class="table-label"><span class="id">Table N</span>[caption — what's being cross-tabulated]</div>
  <table>
    <thead>
      <tr>
        <th>[row label header]</th>
        <th>[col 1]</th>
        <th>[col 2]</th>
        <th>[col 3]</th>
        <th>row total</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>[row 1 label]</td>
        <td class="num">N11</td>
        <td class="num">N12</td>
        <td class="num">N13</td>
        <td class="num">[row 1 total]</td>
      </tr>
      <tr class="highlight">
        <td>[row 2 label — the load-bearing row]</td>
        <td class="num">N21</td>
        <td class="num pos">N22</td>  <!-- highlight the cell that the prose is about -->
        <td class="num">N23</td>
        <td class="num">[row 2 total]</td>
      </tr>
      <tr>
        <td>[row 3 label]</td>
        <td class="num">N31</td>
        <td class="num">N32</td>
        <td class="num">N33</td>
        <td class="num">[row 3 total]</td>
      </tr>
      <tr class="totals">
        <td>column total</td>
        <td class="num">[col 1 total]</td>
        <td class="num">[col 2 total]</td>
        <td class="num">[col 3 total]</td>
        <td class="num">[grand total]</td>
      </tr>
    </tbody>
  </table>
</div>
```

**Conventions:**
- Use `tr.highlight` on the row the prose discusses (typically the "interesting" off-diagonal pattern).
- Use `td.num.pos` on the single cell the prose calls out (e.g. the joint variance-band cell).
- Use `tr.totals` on the column-totals row — adds a top border to separate it from the body.
- Row totals are in the rightmost column; column totals in the bottom row.

---

## 4. Stat-tile row (4 headline numbers)

Use for: section headers where 4 related metrics deserve equal visual weight (compute params, before/after, multi-arm comparison summary).

Template:
```html
<div class="stat-row">
  <div class="stat">
    <span class="k">[label, uppercase]</span>
    <div class="v">[headline number]</div>
    <div class="s">[sublabel — context, units, p-value]</div>
  </div>
  <div class="stat">
    <span class="k">[label]</span>
    <div class="v">[number]</div>
    <div class="s">[sublabel]</div>
  </div>
  <div class="stat">
    <span class="k">[label]</span>
    <div class="v">[number]</div>
    <div class="s">[sublabel]</div>
  </div>
  <div class="stat">
    <span class="k">[label]</span>
    <div class="v">[number]</div>
    <div class="s">[sublabel]</div>
  </div>
</div>
```

**Conventions:**
- Always 4 tiles. (2 tiles per row on mobile, 4 on desktop ≥600px.)
- The `.v` value is short — a number, ratio, or 1–3 word phrase. If it's longer than 3 words, it doesn't belong in a tile.
- The `.s` sublabel carries the context: stderr, p-value, units, ratio components.
- First tile has zero left padding (CSS handles this automatically) so its number aligns with the article column edge.

## When to pick which

| situation | primitive |
|---|---|
| One metric vs continuous x | line trajectory (#1) |
| Two arms compared at 4–8 discrete points | grouped multi-series line (#2) |
| Two-axis cross-tabulation, e.g. arm A × arm B | contingency table (#3) |
| Four headline numbers with equal weight | stat-tile row (#4) |

Don't reach for bar charts (single-bar-per-category) — they're rarely the right fit for the experimental data this skill targets. If you need a bar chart, adapt the grouped line template into bars and ask the user to confirm.

Don't introduce pie charts, scatter plots with 100+ points, heatmaps, or 3D anything. The aesthetic depends on minimalism.
