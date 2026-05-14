# Interactivity patterns

Vanilla JavaScript only. One bottom `<script>` block, IIFE-wrapped. No imports, no React, no jQuery. ES5-ish (`var`, `function`, `forEach`) for legibility — modern syntax works fine but the example collection consistently chooses the older style.

Use these patterns only when the user asked for an interactive artifact (sandbox, editor, sliders, drag-and-drop). A spec or report doesn't need any of this.

## Script-block skeleton

```html
<script>
(function () {
  'use strict';

  // 1. data
  var state = { /* ... */ };

  // 2. render
  function render() {
    // wipe + rebuild the relevant DOM
  }

  // 3. wire events
  document.addEventListener('click', function (e) {
    var t = e.target;
    if (t.matches('[data-action="add"]')) { /* ... */; render(); }
  });

  // 4. initial render
  render();
})();
</script>
```

The IIFE keeps the namespace clean and avoids leaking globals. Event delegation off `document` (or a single root container) keeps the wire-up tight.

---

## Copy-to-clipboard (the most-used pattern)

Every interactive artifact needs at least one copy button. Modern `navigator.clipboard` with a textarea fallback for the rare environment that blocks it.

```html
<button class="btn primary" data-copy>Copy as JSON</button>
<span class="copied" hidden>Copied ✓</span>
```

```js
function copy(text, button) {
  function flash() {
    var msg = button.parentElement.querySelector('.copied');
    if (!msg) return;
    msg.hidden = false;
    setTimeout(function () { msg.hidden = true; }, 1200);
  }
  if (navigator.clipboard) {
    navigator.clipboard.writeText(text).then(flash);
    return;
  }
  // fallback
  var ta = document.createElement('textarea');
  ta.value = text;
  document.body.appendChild(ta);
  ta.select();
  document.execCommand('copy');
  document.body.removeChild(ta);
  flash();
}

document.addEventListener('click', function (e) {
  if (e.target.matches('[data-copy]')) {
    copy(buildExport(), e.target);
  }
});

function buildExport() {
  return JSON.stringify(state, null, 2);
}
```

For "copy as markdown" or "copy as prompt", swap `buildExport()` for a function that emits markdown or a paste-back-into-Claude prompt template.

---

## Drag-and-drop (kanban / triage board)

Native HTML5 drag and drop. Cards have `draggable="true"`; columns are drop targets.

```html
<div class="column" data-bucket="now">
  <h3>Now</h3>
  <div class="cards" data-drop>
    <div class="card-mini" draggable="true" data-id="ENG-101">
      <span class="meta">ENG-101</span>
      <p>Migrate comments table</p>
    </div>
    <!-- ... -->
  </div>
</div>
<div class="column" data-bucket="next">
  <h3>Next</h3>
  <div class="cards" data-drop></div>
</div>
```

```js
var dragging = null;

document.addEventListener('dragstart', function (e) {
  if (e.target.matches('[draggable="true"]')) {
    dragging = e.target;
    e.dataTransfer.effectAllowed = 'move';
    e.target.classList.add('dragging');
  }
});

document.addEventListener('dragend', function (e) {
  if (dragging) dragging.classList.remove('dragging');
  document.querySelectorAll('.dragover').forEach(function (el) {
    el.classList.remove('dragover');
  });
  dragging = null;
});

document.addEventListener('dragover', function (e) {
  var drop = e.target.closest('[data-drop]');
  if (drop) { e.preventDefault(); drop.classList.add('dragover'); }
});

document.addEventListener('dragleave', function (e) {
  var drop = e.target.closest('[data-drop]');
  if (drop) drop.classList.remove('dragover');
});

document.addEventListener('drop', function (e) {
  var drop = e.target.closest('[data-drop]');
  if (!drop || !dragging) return;
  e.preventDefault();
  drop.appendChild(dragging);
  drop.classList.remove('dragover');
  syncStateFromDOM();
});
```

```css
.dragging { opacity: 0.5; }
.dragover { background: rgba(217,119,87,0.06); border-color: var(--clay); }
```

---

## Sliders with live CSS variable swap (animation sandbox)

The most elegant way to bind a slider to a live preview: write to a CSS custom property on `:root` and let the styles read it.

```html
<div class="controls">
  <label>Duration <input type="range" min="100" max="2000" step="50" value="600" data-css="--dur" data-suffix="ms"></label>
  <label>Ease <select data-css="--ease">
    <option value="cubic-bezier(.2,.8,.2,1)">spring</option>
    <option value="ease-in-out">ease-in-out</option>
    <option value="linear">linear</option>
  </select></label>
  <button class="btn" data-trigger>Play</button>
</div>

<div class="preview">
  <button class="checkout">Buy now</button>
</div>
```

```css
.checkout {
  transition: transform var(--dur, 600ms) var(--ease, cubic-bezier(.2,.8,.2,1)),
              background-color var(--dur, 600ms) var(--ease, cubic-bezier(.2,.8,.2,1));
}
.checkout.playing { transform: scale(0.95); background: var(--clay); }
```

```js
document.addEventListener('input', function (e) {
  var t = e.target;
  if (!t.dataset.css) return;
  document.documentElement.style.setProperty(t.dataset.css, t.value);
});

document.addEventListener('click', function (e) {
  if (!e.target.matches('[data-trigger]')) return;
  var btn = document.querySelector('.checkout');
  btn.classList.add('playing');
  setTimeout(function () { btn.classList.remove('playing'); }, 800);
});
```

---

## Tabs

Tabs that swap between panels. Single button row, single content area.

```html
<div class="tabs">
  <button class="tab on" data-tab="js">JavaScript</button>
  <button class="tab"    data-tab="py">Python</button>
  <button class="tab"    data-tab="curl">curl</button>
</div>
<pre class="code panel on" data-panel="js">...</pre>
<pre class="code panel"    data-panel="py">...</pre>
<pre class="code panel"    data-panel="curl">...</pre>
```

```css
.tabs { display: flex; gap: 4px; margin-bottom: 8px; border-bottom: 1.5px solid var(--g300); }
.tab {
  font-family: var(--mono);
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  padding: 8px 12px;
  background: transparent;
  border: none;
  border-bottom: 2px solid transparent;
  color: var(--g500);
  cursor: pointer;
}
.tab.on { color: var(--clay); border-bottom-color: var(--clay); }
.panel { display: none; }
.panel.on { display: block; }
```

```js
document.addEventListener('click', function (e) {
  if (!e.target.matches('[data-tab]')) return;
  var tab = e.target.dataset.tab;
  document.querySelectorAll('.tab').forEach(function (el) { el.classList.toggle('on', el.dataset.tab === tab); });
  document.querySelectorAll('.panel').forEach(function (el) { el.classList.toggle('on', el.dataset.panel === tab); });
});
```

---

## Editable form with live preview (prompt tuner)

Side-by-side: an editable template on the left, a rendered preview on the right that updates as the user types.

```html
<div class="tuner">
  <div class="editor" contenteditable="true" data-template>
    You are a helpful assistant. Answer questions about {{topic}}.
    Be concise — under {{max_words}} words.
  </div>
  <div class="preview" data-preview></div>
</div>
<div class="samples">
  <label>topic <input data-var="topic" value="rate limiting"></label>
  <label>max_words <input data-var="max_words" value="100"></label>
</div>
```

```js
var pendingRender = false;
function scheduleRender() {
  if (pendingRender) return;
  pendingRender = true;
  requestAnimationFrame(function () {
    pendingRender = false;
    render();
  });
}

function render() {
  var tmpl = document.querySelector('[data-template]').innerText;
  var vars = {};
  document.querySelectorAll('[data-var]').forEach(function (el) { vars[el.dataset.var] = el.value; });
  var filled = tmpl.replace(/\{\{(\w+)\}\}/g, function (_, k) { return vars[k] || ''; });
  document.querySelector('[data-preview]').textContent = filled;
}

document.addEventListener('input', scheduleRender);
render();
```

The `requestAnimationFrame` debounce keeps the live preview smooth on slow devices.

---

## Functional state with full re-render (the editor pattern)

For more complex editors (triage board, feature flag editor), keep a single state object and a single `render()` that wipes and rebuilds the DOM. Events mutate state and call `render()`.

```js
var state = {
  tickets: [
    { id: 'ENG-101', title: 'Migrate comments', bucket: 'now', rationale: '' },
    { id: 'ENG-102', title: 'Backfill thread_id', bucket: 'next', rationale: '' },
    // ...
  ]
};

function render() {
  ['now','next','later','cut'].forEach(function (bucket) {
    var col = document.querySelector('[data-bucket="' + bucket + '"] [data-drop]');
    col.innerHTML = '';
    state.tickets
      .filter(function (t) { return t.bucket === bucket; })
      .forEach(function (t) {
        var card = document.createElement('div');
        card.className = 'card-mini';
        card.draggable = true;
        card.dataset.id = t.id;
        card.innerHTML = '<span class="meta">' + t.id + '</span><p>' + escapeHtml(t.title) + '</p>';
        col.appendChild(card);
      });
  });
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, function (c) {
    return { '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;' }[c];
  });
}
```

For tiny state changes (drag-and-drop), it's also fine to mutate the DOM directly and sync state from it (`syncStateFromDOM()`). Use re-render when the change is structural; use direct DOM for one-card-moves.

---

## Keyboard navigation (for slide decks)

```js
document.addEventListener('keydown', function (e) {
  if (e.key === 'ArrowRight' || e.key === ' ') { e.preventDefault(); nextSlide(); }
  if (e.key === 'ArrowLeft')                   { e.preventDefault(); prevSlide(); }
});

function nextSlide() {
  var slides = document.querySelectorAll('.slide');
  var idx = Math.floor(window.scrollY / window.innerHeight);
  if (idx < slides.length - 1) slides[idx + 1].scrollIntoView({ behavior: 'smooth' });
}
function prevSlide() {
  var idx = Math.floor(window.scrollY / window.innerHeight);
  if (idx > 0) document.querySelectorAll('.slide')[idx - 1].scrollIntoView({ behavior: 'smooth' });
}
```

---

## Anti-patterns for interactivity

- **No `addEventListener` per element.** Use event delegation off `document` or a root container. Cleaner, survives re-renders.
- **No `innerHTML = state.map(...)`.** Use `document.createElement` + `appendChild` so user input doesn't have to be escaped manually.
- **No async/await without a try/catch.** Browsers swallow unhandled promise rejections silently in some contexts.
- **No `setInterval` for "live update" loops.** Use `requestAnimationFrame` with a flag.
- **No fetching from external URLs.** The artifact is offline-first. If the user needs to fetch data, ask them to paste it into the page first.
- **No alert(), confirm(), prompt().** Inline a confirmation row instead.
- **No localStorage unless the user explicitly asked for "remember my settings".** The artifact is throwaway by default.

---

## Export-back-to-Claude pattern

Every interactive artifact ends with a "Copy as prompt" button that produces text the user can paste back into Claude Code. This closes the loop.

```js
function exportAsPrompt() {
  return [
    "Here's the final triage from the HTML editor:",
    "",
    "## Now",
    state.tickets.filter(function (t) { return t.bucket === 'now'; })
      .map(function (t) { return '- ' + t.id + ' — ' + t.title; }).join('\n'),
    "",
    "## Next",
    state.tickets.filter(function (t) { return t.bucket === 'next'; })
      .map(function (t) { return '- ' + t.id + ' — ' + t.title; }).join('\n'),
    "",
    "Please now generate the sprint plan based on the Now column."
  ].join('\n');
}
```

The exported text should be immediately useful — not a JSON dump. It includes a leading sentence of context and a trailing sentence telling Claude what to do next. This is what makes the round-trip feel like a tool, not a toy.
