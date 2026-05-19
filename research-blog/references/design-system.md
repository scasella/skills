# Design system reference

Every CSS token, layout primitive, and component class used in `assets/template.html`. Read this when verifying a token or extending a component.

## Color tokens

```css
--bg:           #F9F9F6;  /* page background — warm off-white */
--accent:       #090909;  /* near-black — body text base, footer bg, link color */
--fg:           #3B3B39;  /* warm dark gray — headings + body prose */
--fg-soft:      #3B3B39;  /* same as --fg, kept separate for future divergence */
--fg-mute:      #595856;  /* secondary labels, callout body */
--fg-faint:     #969592;  /* tertiary — date, dotted underline, axis labels */
--on-dark:      #DFDEDA;  /* footer body text on dark bg */
--surface-muted:#EFEFEB;  /* callout fill, highlight row tint */

/* Chart palette — muted earth tones */
--chart-primary:   #3B3B39;  /* primary series stroke (matches body text) */
--chart-secondary: #969592;  /* baseline / comparison series */
--chart-axis:      #C8C7C2;  /* axis line */
--chart-grid:      #E4E3DE;  /* gridlines + table dividers */
--chart-accent-1:  #5C8A95;  /* sage-teal — single-series line charts */
--chart-accent-2:  #8B6F8C;  /* dusty mauve — third series when needed */
```

**Rules:**
- Do not introduce saturated colors (red, blue, green at full saturation). The palette is monochromatic warm gray plus two muted earth accents. Adding bright color breaks the editorial register.
- For positive deltas in tables use `td.pos { color: var(--accent) }` (not green). For negative or muted deltas use `td.neg { color: var(--fg-faint) }` (not red). Sign + tabular-nums conveys direction.
- The footer is the only dark surface on the page. Don't add dark callouts or dark cards in the body — they break the "single dark anchor" pattern.

## Typography

```css
--font-serif: 'Libre Baskerville', Georgia, 'Times New Roman', serif;
--font-sans:  'Inter', 'Helvetica Neue', Arial, sans-serif;
```

| element | font | size | weight | notes |
|---|---|---:|---:|---|
| H1 (article title) | serif | 48px | 400 | line-height 1.1, margin-top 144px |
| Subtitle | serif | 18px | 300 | sits directly under H1 |
| Date / byline | sans | 11px | – | uppercase, letter-spacing 0.1em |
| H2 | serif | 26px | 400 | margin-top 1.75lh, no `#` prefix decoration |
| H3 | serif | 19px | **700** | bold to anchor sub-sections at this small size |
| Body p / li | serif | 17px | 400 | line-height 1.6 |
| TL;DR p | serif | 17px | 400 | left-rule pulled-quote treatment |
| Callout p | serif | 15px | 400 | inside warm-tinted card |
| Stat tile value | serif | 24px | 400 | tabular-nums, letter-spacing -0.01em |
| Stat tile label | sans | 11px | – | uppercase, letter-spacing 0.12em |
| Stat tile sublabel | sans | 12px | 400 | faint |
| Table th | sans | 12px | 400 | uppercase, letter-spacing 0.06em, color fg-mute |
| Table td | serif | 14px | 400 | tabular-nums |
| Mode card title | serif | 17px | **700** | |
| Mode card desc | serif | 14px | 400 | |
| Neg-list item | serif | 15px | 400 | |
| Code (inline) | mono | 0.82em | – | rgba(0,0,0,0.05) bg |
| Footer subscribe label | serif | 17px | 400 | on dark bg, color on-dark |
| Footer meta | sans | 12px | – | color fg-faint on dark bg |

**Rules:**
- Italic only on defined concepts (e.g. *variance band*, *Base*) — not for emphasis. Use `<strong>` (weight 500, color fg) for emphasis instead.
- All numbers in tables and stat tiles use `font-variant-numeric: tabular-nums` (already set on `table` and stat values).
- Line-height: body 1.6, headings 1.1–1.5. Don't tighten body below 1.5.

## Layout primitives

| primitive | role |
|---|---|
| `.page-surface` | flex column wrapping header + main + footer |
| `.perspectives-header` | sticky-feeling top bar with logo left, contact link right (padding 2rem 2.5rem) |
| `.benchmarks-content` | article column, `max-width: 720px`, centered, `padding: 2rem 2rem 6rem` |
| `.benchmarks-body` | article body wrapper inside `.benchmarks-content`, `margin: 96px 0 48px` |
| `.body-main` | actual prose container — anchor for chart breakouts |
| `.site-footer` | dark bg, max-width 720px inner, padding-bottom 140px |

**Column width:** 720px. The article column is exactly 720px on desktop, gutters at 2rem. This is the load-bearing constraint that gives the page its readable, editorial proportion. Don't widen the body column.

**Chart breakout:** Charts sized as direct children of `.body-main` break out wider:
- ≥960px viewport: `width: min(1200px, 100vw - 3rem)`, centered via `margin-left: 50%; transform: translateX(-50%)`
- ≥1400px viewport: `width: min(1320px, 100vw - 3rem)`
- The selector is `.body-main > figure.chart` — figures must be direct children for the breakout to apply.

## Components

### `.tldr` — pulled-quote with left rule
- 2px left border in `--fg-mute`, 24px left padding, 32px top / 48px bottom margin
- `.tldr-label` is uppercase 11px sans
- `.tldr p` is 17px serif weight 400, line-height 1.6

### `.callout` — boxed aside
- Background `--surface-muted`, border-radius 10px, padding 20px 24px
- `.callout-label` is uppercase 11px sans
- `.callout p` is 15px serif weight 400 — slightly smaller than body
- Use for callouts that interrupt the main argument. Do not nest callouts.

### `.stat-row` — minimal number tiles
- 4-column grid on desktop, 2-column on mobile
- Top + bottom borders in `--chart-grid`; vertical dividers in `--chart-grid`
- First cell has zero left padding so its number aligns with the article column
- `.stat .v` is the headline number (24px serif), `.k` is the uppercase label, `.s` is the sublabel (12px sans, faint)
- 4 tiles per row is the convention. 2 or 3 work but feel under-used.

### `.mode-grid` + `.mode-card` — method-step cards
- 2-column grid of bordered white cards
- Each card has `.tag` (uppercase tracker), `.t` (title, 17px bold serif), `.desc` (14px serif body)
- Use for procedural / methodology breakdowns where four discrete sub-steps deserve equal visual weight
- 4 cards in a 2×2 grid is the typical use

### `.table-wrap` + `<table>` — data tables
- `.table-label` above table: uppercase sans, 11px, with `.id` for the table number (e.g. "Table 03")
- Hairline borders in `--chart-grid`
- `tr.highlight` tints the row in `--surface-muted`
- `tr.totals` adds a heavier top border (the column-totals row)
- `td.num` for numerical cells, `td.pos` / `td.neg` for delta sign coloring

### `figure.chart` — charts with caption
- Direct child of `.body-main` to get the breakout width
- `<svg>` inside, `viewBox` provides internal coordinate space (typical: 960×460 or 760×320)
- `<figcaption>` below: 13px sans, line-height 1.5, color fg-mute
- Use `<strong>` inside figcaption to call out the figure number ("**Figure 1.**")

### `.neg-list` — honest-scope list
- Uses `<ul>` with custom styling: no bullets, hairline horizontal dividers between items
- Each `<li>` has heavy top dot via `<strong>` for category ("**Does say:**", "**Does not say:**")
- Use exactly once per article, in or near the bounds-on-the-claim section

### `.break` — section divider
- Three letter-spaced dots: `· · ·`
- Use sparingly — once before the closing two paragraphs, never inside a section

## Header + footer

**Header:**
```html
<header class="perspectives-header">
  <a href="#" class="logo-centered">MULTI<span class="accent">·</span>MODEL</a>
  <a href="mailto:contact@example.com" class="contact-link">Contact</a>
</header>
```
Customize the logo for the user's lab/project name. Keep the format: tracked uppercase sans with an accent dot.

**Footer:**
```html
<footer class="site-footer">
  <div class="footer-inner">
    <form class="footer-subscribe" novalidate>
      <label class="footer-subscribe-label" for="footer-email">Get early access to research, products, and more.</label>
      <div class="footer-subscribe-row">
        <input class="footer-subscribe-input" type="email" id="footer-email" placeholder="you@example.com" />
        <button class="footer-subscribe-button" type="submit">Subscribe</button>
      </div>
    </form>
    <div class="footer-meta">
      Author · org · date<br />
      Backbone / model / setup info<br />
      Code &amp; data: <a href="#">manifest</a> · <a href="#">scripts</a>
    </div>
  </div>
</footer>
```
The subscribe form is presentational — no submit handler is wired. If the user wants a working form, ask them for the endpoint and add a `fetch` POST in inline JS, or mention it as a follow-up.

## Responsive

Two breakpoints, mirroring the source design:

```css
@media (max-width: 768px) {
  .perspectives-header { padding: 1.5rem 1.5rem; }
  .benchmarks-content { padding: 3rem 1.5rem 4rem; }
  .benchmarks-content h1 { font-size: 44px; margin-top: 120px; }
  .benchmarks-body { margin: 72px 0 32px; }
  .site-footer .footer-inner { padding-left: 1.5rem; padding-right: 1.5rem; }
}
@media (max-width: 480px) {
  .perspectives-header { padding: 1.25rem 1.25rem; }
  .benchmarks-content { padding: 2rem 1.25rem 3rem; }
  .benchmarks-content h1 { font-size: 38px; margin-top: 80px; }
  .benchmarks-content .subtitle { font-size: 18px; }
  .benchmarks-body h2 { font-size: 26px; }
  .benchmarks-body h3 { font-size: 20px; }
  .benchmarks-body .body-main { font-size: 18px; }
  .benchmarks-body li { font-size: 18px; }
  .tldr p { font-size: 18px; }
  .stat .v { font-size: 24px; }
  .site-footer .footer-inner { padding: 0 1.25rem 80px; }
}
```

These are already in the template. Don't add a third breakpoint unless the user explicitly needs it.
