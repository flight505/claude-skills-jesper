# HTML Template — single-file lesson starter

Every lesson is one `.html` file that opens in any browser with zero build step. This document is the canonical starter Claude fills in. The contents of `lesson-base.css` are inlined directly so the lesson works fully offline once the CDN libs are cached.

## Layout model (v2 — CSS Grid breakout)

The article is a **3-column grid**: `[gutter | content | gutter]`. Children default to the centered `content` lane (38em measure, comfortable for prose). Anything that needs more room — widgets, wide SVGs, the worked-example scrubber — opts into the `breakout` lane up to 56em.

On wide screens (≥1280px), the page becomes a 2-track outer grid with the concept-map TOC docked sticky-left. On narrower screens the TOC collapses to a `<details>` dropdown at the top of the article.

```
┌──── viewport ────────────────────────────────────────────────┐
│  ┌── .lesson (max 1280px, centered) ────────────────────┐    │
│  │  ┌─ TOC ──┐   ┌─── article (grid) ──────────────────┐│    │
│  │  │ 1.     │   │     prose (content lane, 38em)      ││    │
│  │  │ 2.     │   │  ┌─── widget (breakout lane, 56em) ─┐│    │
│  │  │ 3. ✦   │   │  │   slider, SVG, controls          ││    │
│  │  │ 4.     │   │  └──────────────────────────────────┘│    │
│  │  └────────┘   │     prose                            ││    │
│  │   sticky      └──────────────────────────────────────┘│    │
│  └─────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

## Hard rules (the new "viewport-base" equivalent)

These are non-negotiable. Like `frontend-slides`' viewport-base.css, they catch the most common shape failures by construction.

1. **Always inline `lesson-base.css` verbatim** into the `<style>` block. No external stylesheets except CDN libs.
2. **Wrap the whole page in `<div class="lesson">`** + `<article>`. Don't bypass the grid.
3. **Every widget must be a `<div class="widget">`** so it gets the breakout lane + card frame.
4. **Every SVG inside a widget**: use `viewBox` only, never fixed `width` / `height`. `lesson-base.css` makes them responsive automatically.
5. **Never duplicate a `<pre>` matrix as an SVG matrix and vice versa.** Pick one representation per data point. SVG matrices are for heatmap-style data where color carries info; text matrices are for precise inspection. Showing both creates visual clutter without learning gain.
6. **Mobile concept-map**: include BOTH `<details class="concept-map-mobile">` (shown <1280px) AND `<nav class="concept-map-fixed">` (shown ≥1280px) — same content, two presentations. The CSS handles which is visible.
7. **Color-code variables across prose, equation, and diagram** using the same hex. Q=`#ffb86c`, K=`#6ab0e8`, V=`#b0d977` (defaults), then `\color{}` in the LaTeX matches the CSS variable color.
8. **Math display blocks**: `lesson-base.css` allows `.katex-display` to scroll horizontally on narrow screens — don't try to break long equations manually.
9. **TOC ↔ section invariant**: every `<li data-section="X">` in the concept-map must match an existing `<section id="X">`, and vice versa. Both directions are enforced by the linter. Mismatch = silent TOC failure.
10. **Run `scripts/lesson-lint.py <file>` before opening.** This is the mandatory Layer-A QA gate. See SKILL.md Phase 3.5a. The linter catches missing required elements, broken TOC pointers, oversized fixed-width SVGs in widgets, and unfilled placeholders.

## The Starter

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{title}}</title>
<meta name="description" content="{{topic_blurb}}">

<!-- ============================================================
     ALWAYS-LOADED: typography & math
     ============================================================ -->

<!-- Tufte CSS for sidenote utilities (optional — drop if not used) -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/edwardtufte/tufte-css@gh-pages/tufte.min.css">

<!-- KaTeX for math rendering -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script defer
  src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"
  onload="renderMathInElement(document.body,{delimiters:[
    {left:'$$',right:'$$',display:true},
    {left:'$',right:'$',display:false}
  ], throwOnError:false})"></script>

<!-- OPTIONAL CDN libs — uncomment only if used in this lesson -->
<!-- Scrollytelling: <script defer src="https://cdn.jsdelivr.net/npm/scrollama@3.2.0/build/scrollama.min.js"></script> -->
<!-- Mermaid:       <script type="module">import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs'; mermaid.initialize({startOnLoad:true, theme:'neutral'});</script> -->
<!-- Anime.js:      <script type="module">import {animate,stagger} from 'https://cdn.jsdelivr.net/npm/animejs@4/lib/anime.esm.min.js'; window.animate=animate; window.stagger=stagger;</script> -->
<!-- Comparison:    <script type="module" src="https://cdn.jsdelivr.net/npm/img-comparison-slider@8/dist/index.js"></script><link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/img-comparison-slider@8/dist/styles.css"> -->

<style>
/* >>> INLINE THE FULL CONTENTS OF lesson-base.css HERE <<< */
/* (plus any per-lesson preset overrides — see STYLE_PRESETS.md) */
</style>

</head>
<body>

<div id="progress"></div>

<div class="lesson">

  <!-- Sticky TOC (visible ≥1280px) -->
  <nav class="concept-map-fixed" aria-label="Lesson outline">
    <div class="concept-map">
      <ol>
        <li data-section="motivation">1. Motivation</li>
        <li data-section="intuition">2. Build the intuition</li>
        <li data-section="mechanics">3. How it works</li>
        <li data-section="example">4. Worked example</li>
        <li data-section="failure">5. Where it breaks</li>
        <li data-section="recap">6. Recap & retrieval</li>
      </ol>
    </div>
  </nav>

  <article>

    <header>
      <h1>{{title}}</h1>
      <p class="subtitle">{{topic_blurb}}</p>
    </header>

    <!-- Collapsed TOC for narrow screens (auto-hidden ≥1280px) -->
    <details class="concept-map-mobile">
      <summary>Lesson outline</summary>
      <nav class="concept-map" aria-label="Lesson outline">
        <ol>
          <li data-section="motivation">1. Motivation</li>
          <li data-section="intuition">2. Build the intuition</li>
          <!-- mirror the fixed TOC -->
        </ol>
      </nav>
    </details>

    <!-- ============================================================
         SECTION 1 — Motivation (puzzle, NOT definition)
         ============================================================ -->
    <section id="motivation">
      <h2>The puzzle</h2>

      <p>
        Open with a concrete scenario or surprising observation. NOT a definition.
        Make the reader feel the question before showing the answer.
      </p>

      <div class="widget">
        <!-- Tiny interactive that demonstrates the puzzle.
             SVG inside uses viewBox, never fixed width. -->
        <svg viewBox="0 0 600 240" role="img" aria-label="…"></svg>
      </div>

      <p class="socratic">
        What do you think happens when X gets very large? Try the slider above
        before reading on.
      </p>

      <button class="ask-claude"
              data-prompt="In the lesson on {{title}}, give me three more real-world examples where this puzzle shows up.">
        💬 Ask Claude for more examples
      </button>
    </section>

    <!-- ============================================================
         SECTION 2 — Intuition (ADEPT order, with wrong-intuition callout)
         ============================================================ -->
    <section id="intuition">
      <h2>Building the intuition</h2>

      <article class="adept">
        <h3>{{concept_name}}</h3>
        <p><strong>Analogy:</strong> …</p>
        <div><!-- SVG / Mermaid diagram --></div>
        <p><strong>Example:</strong> …</p>
        <p><strong>Plain English:</strong> …</p>
        <p><strong>Technical:</strong> $…$</p>
      </article>

      <aside class="wrong-intuition">
        <h4>⚠️ A common wrong intuition</h4>
        <p>…</p>
      </aside>

      <button class="ask-claude"
              data-prompt="In the lesson on {{title}}, give me another analogy for {{concept_name}} that highlights a different aspect of how it works.">
        💬 Ask Claude for an alternative analogy
      </button>
    </section>

    <!-- ============================================================
         SECTION 3 — Mechanics (triptych: prose + visual + symbolic)
         ============================================================ -->
    <section id="mechanics">
      <h2>How it actually works</h2>

      <p>
        The relationship between <span class="var-x">x</span> and
        <span class="var-y">y</span> is …
      </p>
      <p>$$\color{#c33}{x}^2 + \color{#39c}{y}^2 = r^2$$</p>

      <div class="widget">
        <!-- interactive that lets the reader manipulate x and y -->
      </div>

      <div class="predict">
        <p class="predict-q">If we double <span class="var-x">x</span>, what happens to <span class="var-y">y</span>?</p>
        <input class="predict-input" placeholder="your guess">
        <button class="predict-reveal">Reveal</button>
        <p class="predict-a" hidden>…</p>
      </div>
    </section>

    <!-- ============================================================
         SECTION 4 — Worked example (step-through scrubber)
         ============================================================ -->
    <section id="example">
      <h2>A worked example</h2>
      <p>Walk through one concrete instance, one decision at a time.</p>

      <div class="widget">
        <div class="step-controls">
          <button data-step="-1">◀ Prev</button>
          <input type="range" id="t" min="0" max="4" value="0">
          <button data-step="1">Next ▶</button>
          <span class="readout">Step <strong id="step-i">0</strong>/4</span>
        </div>
        <p class="step-caption" id="step-cap">—</p>
        <!-- Use <pre> for precise matrix inspection; SVG for heatmaps.
             NEVER both for the same data. -->
        <pre id="step-state">—</pre>
      </div>
    </section>

    <!-- ============================================================
         SECTION 5 — Failure modes (diagnostic quiz)
         ============================================================ -->
    <section id="failure">
      <h2>Where it breaks</h2>
      <p>The success path teaches the rules. The failure path teaches the intuition.</p>

      <div class="quiz" data-correct="b">
        <p class="quiz-q">…</p>
        <button data-k="a">…</button>
        <button data-k="b">…</button>
        <button data-k="c">…</button>
        <p class="quiz-fb" data-fb="a" hidden>…</p>
        <p class="quiz-fb correct" data-fb="b" hidden>…</p>
        <p class="quiz-fb" data-fb="c" hidden>…</p>
      </div>
    </section>

    <!-- ============================================================
         SECTION 6 — Recap & retrieval
         ============================================================ -->
    <section id="recap">
      <h2>Recap</h2>
      <p>The one-line takeaway.</p>

      <section class="retrieval">
        <h4>Before you close this tab…</h4>
        <ol>
          <li>In your own words, what does {{concept_name}} mean?</li>
          <li>What's the most common wrong intuition, and why is it wrong?</li>
          <li>Sketch (mentally) what happens when X is at its extreme.</li>
        </ol>
      </section>

      <button class="ask-claude"
              data-prompt="I just finished the lesson on {{title}}. Quiz me — ask me three increasingly difficult questions about it, and tell me where my mental model is weak.">
        💬 Ask Claude to quiz me
      </button>
    </section>

  </article>
</div>

<!-- ============================================================
     SCRIPTS
     ============================================================ -->
<script>
  // Progress bar
  addEventListener('scroll', () => {
    progress.style.width =
      (scrollY / (document.body.scrollHeight - innerHeight) * 100) + '%';
  });

  // Concept-map highlight (both fixed and mobile share data-section)
  const obs = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        document.querySelectorAll('.concept-map li').forEach(li => li.classList.remove('active'));
        document.querySelectorAll(`.concept-map [data-section="${e.target.id}"]`).forEach(li => li.classList.add('active'));
      }
    });
  }, {rootMargin: '-40% 0px -40% 0px'});
  document.querySelectorAll('article section[id]').forEach(s => obs.observe(s));

  // Predict-then-reveal
  document.querySelectorAll('.predict-reveal').forEach(b =>
    b.addEventListener('click', () => b.nextElementSibling.hidden = false));

  // Quiz feedback
  document.querySelectorAll('.quiz button').forEach(b => b.addEventListener('click', () => {
    const q = b.closest('.quiz');
    q.querySelectorAll('.quiz-fb').forEach(p => p.hidden = true);
    q.querySelector(`[data-fb="${b.dataset.k}"]`).hidden = false;
  }));

  // Ask-Claude clipboard
  document.querySelectorAll('.ask-claude').forEach(b => b.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(b.dataset.prompt);
      const orig = b.textContent;
      b.textContent = '✓ Copied — paste into Claude Code';
      setTimeout(() => b.textContent = orig, 2500);
    } catch (e) {
      b.textContent = 'Copy failed — see console';
      console.error(e);
    }
  }));

  // Step-through scrubber widget. Replace `steps` and the IDs to match your lesson.
  // The widget needs: button[data-step], input[type=range]#t, span#step-i,
  //                   p#step-cap (caption), pre#step-state (state dump).
  (() => {
    const t = document.getElementById('t');
    if (!t) return;  // No step-through widget in this lesson — skip.
    const iLbl = document.getElementById('step-i');
    const cap = document.getElementById('step-cap');
    const st = document.getElementById('step-state');

    // EDIT THIS: one frame per step. cap is the plain-English caption; state is the dump.
    const steps = [
      {cap: 'Step 0 — initial state.', state: '<replace with your data>'},
      {cap: 'Step 1 — first transformation.', state: '...'},
      {cap: 'Step 2 — second.', state: '...'},
      {cap: 'Step 3 — third.', state: '...'},
      {cap: 'Step 4 — result.', state: '...'},
    ];
    const max = steps.length - 1;
    t.max = max;

    function render() {
      const i = +t.value;
      if (iLbl) iLbl.textContent = i;
      cap.textContent = steps[i].cap;
      st.textContent = steps[i].state;
    }
    document.querySelectorAll('[data-step]').forEach(b =>
      b.addEventListener('click', () => {
        t.value = Math.max(0, Math.min(max, +t.value + (+b.dataset.step)));
        render();
      }));
    t.addEventListener('input', render);
    render();
  })();
</script>

</body>
</html>
```

## Required structural elements (Quality Bar)

Verify before opening:

- [ ] Page wrapped in `<div class="lesson">` containing `<article>` (grid layout)
- [ ] Every widget is `<div class="widget">` (gets breakout + card)
- [ ] No SVG with fixed `width`/`height` — all use `viewBox` only
- [ ] No `<pre>` and SVG showing the same data side by side
- [ ] Both `concept-map-fixed` and `concept-map-mobile` are present (responsive)
- [ ] At least 4 `.ask-claude` buttons with specific `data-prompt` text
- [ ] Color-coded variables (`.var-q`, `.var-k`, `.var-v` etc.) used consistently across prose + equations + SVG fills
- [ ] `lesson-base.css` inlined in `<style>` block
- [ ] `prefers-reduced-motion` respected (handled by lesson-base.css)
- [ ] Reading-progress bar present

## File naming & location

```
lessons/
  YYYY-MM-DD-kebab-slug.html
  YYYY-MM-DD-kebab-slug.meta.json   # title, source, preset, central misconception
```

Single self-contained `.html`. Never a folder of assets.
