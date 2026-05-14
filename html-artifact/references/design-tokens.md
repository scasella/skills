# Design tokens

Paste these into the `<style>` block at the top of every HTML artifact you generate. Do not modify the values — the consistency across artifacts is what makes them feel like a coherent family.

## CSS variables (paste verbatim)

```css
:root {
  /* ── neutrals (the paper-and-clay palette) ─────────── */
  --ivory:  #FAF9F5;   /* page background */
  --paper:  #FFFFFF;   /* cards, panels */
  --slate:  #141413;   /* primary text + dark surfaces */
  --g100:   #F0EEE6;   /* subtle row fills */
  --g200:   #E6E3DA;   /* hover fills */
  --g300:   #D1CFC5;   /* universal border */
  --g500:   #87867F;   /* muted/meta text, mono labels */
  --g700:   #3D3D3A;   /* body text */

  /* ── accent + semantics ────────────────────────────── */
  --clay:    #D97757;  /* THE accent — links, primary, italic em */
  --clay-d:  #B85C3E;  /* clay hover */
  --oat:     #E3DACC;  /* warm tan — avatars, secondary fills */
  --olive:   #788C5D;  /* success / additions */
  --rust:    #B04A3F;  /* danger / deletions */
  --amber:   #C78E3F;  /* warning */
  --steel:   #5C7CA3;  /* info */

  /* ── typography stacks ─────────────────────────────── */
  --serif: ui-serif, Georgia, "Times New Roman", Times, serif;
  --sans:  system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  --mono:  ui-monospace, "SF Mono", Menlo, Monaco, Consolas, monospace;
}
```

**Why these specific values?** They are taken verbatim from the reference example collection. The cream `#FAF9F5` reads warmer than the standard near-white `#FAFAFA` Material/Tailwind grays, which signals "thoughtful editorial document" rather than "SaaS dashboard." Clay `#D97757` is a muted terracotta, not the saturated orange most AI HTML reaches for.

## Typography rules (rigid)

The three font stacks have rigid role assignments. Mixing them is the most identifying detail of the aesthetic.

| Role | Stack | Rule |
|---|---|---|
| Headings (h1, h2, h3) | `--serif` | `font-weight: 500` (never 600/700). Letter-spacing `-0.01em` to `-0.02em`. Line-height `1.06` for h1, `1.15` for h2, `1.25` for h3. |
| Body text | `--sans` | 14–16px. Line-height 1.5–1.65. Color `--g700` (never pure black). |
| Eyebrows, file paths, badges, code, line numbers, timestamps, hex codes | `--mono` | 10–13px. Uppercase eyebrows with `letter-spacing: 0.08–0.12em`, color `--g500`. |

### Heading sizes

```css
h1 {
  font-family: var(--serif);
  font-weight: 500;
  font-size: clamp(38px, 5.4vw, 62px);
  line-height: 1.06;
  letter-spacing: -0.018em;
  margin: 0 0 8px;
}
h1 em { font-style: italic; color: var(--clay); }  /* signature touch */

h2 {
  font-family: var(--serif);
  font-weight: 500;
  font-size: clamp(22px, 2.4vw, 28px);
  line-height: 1.18;
  letter-spacing: -0.012em;
  margin: 0 0 10px;
}

h3 {
  font-family: var(--serif);
  font-weight: 500;
  font-size: 18px;
  letter-spacing: -0.005em;
  margin: 0 0 6px;
}
```

### Body

```css
body {
  margin: 0;
  background: var(--ivory);
  color: var(--slate);
  font-family: var(--sans);
  font-size: 15px;
  line-height: 1.55;
  -webkit-font-smoothing: antialiased;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
```

### Links

```css
a {
  color: var(--clay);
  text-decoration-color: var(--oat);
  text-underline-offset: 3px;
}
a:hover { text-decoration-color: var(--clay); }
```

## Spacing scale

Use a 4-based scale. Never invent arbitrary values like `padding: 13px 19px`.

| Token | Value | Use |
|---|---|---|
| xs | 4px | Tight gaps inside chips |
| sm | 8px | Inline gaps |
| md | 12px | Default flex gap |
| lg | 16px | Card padding (compact) |
| xl | 24px | Section internal padding |
| 2xl | 32px | Page side padding |
| 3xl | 48px | Section margin |
| 4xl | 64px | Major section separation |

Card padding: 16–28px. Section gaps: 40–64px. Bottom-of-page padding: 96–140px (large white space below content is a hallmark).

## Border radii

| Element | Radius |
|---|---|
| Pill / badge / tag | `999px` |
| Card / panel | `10–14px` |
| Row / list item | `8–10px` |
| Diff row / code block | `6–8px` |
| Button (rectangular) | `8–10px` |

**Never use radii larger than 14px on cards.** The chunky `rounded-2xl` look is a generic-AI tell.

## Borders

**1.5px borders everywhere.** Not 1px (too thin), not 2px (too heavy). It is the single most identifying visual detail.

```css
.card { border: 1.5px solid var(--g300); border-radius: 12px; }
```

The only exception is inner separator lines (`border-bottom: 1px solid var(--g100)` between table rows), which can be 1px.

## Shadows

Default: no shadow.

Card hover: `box-shadow: 0 10px 30px rgba(20,20,19,.10);` paired with `transform: translateY(-2px)` and `border-color: var(--slate);`.

That is the only shadow. No multi-layer Material shadows, no glow effects.

## Layout container

```css
.wrap {
  max-width: 1120px;   /* 720–880px for long-form prose pages */
  margin: 0 auto;
  padding: 0 32px 120px;
}
```

Page content widths:
- Long-form prose / explainer: 720–820px
- Mixed prose + diagrams: 880–960px
- Editor / dashboard / mosaic: 1120–1240px
- Slide deck: 100vw with internal 1080px slides

## Mobile breakpoint

One breakpoint per page. Standard:

```css
@media (max-width: 880px) {
  .wrap { padding: 0 20px 80px; }
  .grid-2, .grid-3 { grid-template-columns: 1fr; }
  .toc-sidebar { display: none; }
}
```

Use 640px for tighter layouts, 920px for explainer pages with a TOC sidebar.

## Semantic surface fills

Never solid green/red/yellow for status backgrounds. Use 10–16% alpha of the semantic color over white:

```css
.chip.success { background: rgba(120,140,93,.16); color: var(--olive); }
.chip.danger  { background: rgba(176,74,63,.16);  color: var(--rust); }
.chip.warning { background: rgba(199,142,63,.18); color: var(--amber); }
.chip.info    { background: rgba(92,124,163,.16); color: var(--steel); }
.chip.neutral { background: var(--g100);           color: var(--g700); }
```

## The signature eyebrow

The page kicker — a small mono uppercase label preceded by a clay tick. Use it as the first element under the masthead.

```css
.eyebrow {
  font-family: var(--mono);
  font-size: 12px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--g500);
  margin-bottom: 18px;
  display: flex;
  align-items: center;
  gap: 12px;
}
.eyebrow::before {
  content: "";
  width: 24px; height: 1.5px;
  background: var(--clay);
}
```

```html
<div class="eyebrow">Spec · v2 draft</div>
<h1>Comment threads on <em>task cards</em></h1>
```

## What to vary, what to lock

**Lock** (every artifact uses these unchanged):
- the palette
- the three font stacks and their role assignments
- 1.5px borders
- ivory page background

**Vary** (per artifact):
- which sections/components appear (depends on use case)
- the heading copy
- max-width (long prose vs wide editor)
- which one of olive/rust/amber/steel semantic colors appears
