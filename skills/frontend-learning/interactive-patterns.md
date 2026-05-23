# Interactive Patterns — Widget Library

Copy-paste HTML/JS for the widgets every lesson page should choose from. All snippets are self-contained, zero-build, single-file friendly. Pick patterns based on the *pedagogical* need (see [pedagogy-principles.md](pedagogy-principles.md)) — never include a widget just because it looks cool.

**Stack assumptions:** the lesson loads KaTeX, Tufte CSS, scrollama, optionally Mermaid and anime.js. See [html-template.md](html-template.md) for the always-included header.

---

## 1. Draggable Slider → Live Visualization

What: a `<input type=range>` bound to a number, formula, and SVG. The slider IS the lesson — Ciechanowski's signature move.
Pedagogical use: any concept with a free parameter (gravity, learning rate, sample size, interest rate). Show equation + picture updating together.

```html
<div class="widget">
  <label>Mass: <input type="range" id="m" min="1" max="100" value="20"></label>
  <span id="mv">20</span> kg · F = <span id="f">196</span> N
  <svg width="200" height="200" viewBox="0 0 200 200">
    <circle id="ball" cx="100" cy="100" r="20" fill="var(--accent)"/>
  </svg>
</div>
<script>
  (() => {
    const m = document.getElementById('m');
    const update = () => {
      mv.textContent = m.value;
      f.textContent = (m.value * 9.8).toFixed(1);
      ball.setAttribute('r', 5 + m.value/3);
    };
    m.addEventListener('input', update);
    update();
  })();
</script>
```

---

## 2. Predict-Then-Reveal Card

What: hide the answer behind a button; force the reader to commit a guess first (Quantum Country / Matuschak pattern).
Pedagogical use: any non-obvious result. Activates retrieval; doubles retention.

```html
<div class="predict">
  <p class="predict-q">What happens to the period if you double the pendulum length?</p>
  <input class="predict-input" placeholder="your guess">
  <button class="predict-reveal">Reveal</button>
  <p class="predict-a" hidden>
    It increases by √2 ≈ 1.41×. The period scales with √L, not L —
    so doubling length only multiplies the period by about 41%, not 100%.
  </p>
</div>
<script>
  document.querySelectorAll('.predict-reveal').forEach(b =>
    b.addEventListener('click', () => b.nextElementSibling.hidden = false));
</script>
```

---

## 3. Step-Through Animation (scrubbable + next)

What: an array of "frames" plus a slider and Next/Prev buttons. Reader controls time.
Pedagogical use: algorithms (sorting, gradient descent), proofs, mechanisms with sequential phases.

```html
<div class="widget">
  <button data-step="-1">◀ Prev</button>
  <input type="range" id="t" min="0" max="5" value="0">
  <button data-step="1">Next ▶</button>
  <pre id="state" class="step-state"></pre>
  <p id="caption" class="step-caption"></p>
</div>
<script>
  (() => {
    const frames = [
      {state: [3,1,4,1,5], caption: 'Start: unsorted'},
      {state: [1,3,4,1,5], caption: 'Swap 3 and 1'},
      {state: [1,3,1,4,5], caption: 'Swap 4 and 1'},
      {state: [1,1,3,4,5], caption: 'Swap 3 and 1'},
      {state: [1,1,3,4,5], caption: 'No swap needed'},
      {state: [1,1,3,4,5], caption: 'Sorted!'},
    ];
    const t = document.getElementById('t');
    const render = () => {
      const f = frames[+t.value];
      state.textContent = JSON.stringify(f.state);
      caption.textContent = f.caption;
    };
    t.addEventListener('input', render);
    document.querySelectorAll('[data-step]').forEach(b =>
      b.addEventListener('click', () => {
        t.value = Math.max(0, Math.min(frames.length-1, +t.value + (+b.dataset.step)));
        render();
      }));
    render();
  })();
</script>
```

---

## 4. Toggleable Annotation Layers

What: checkboxes that show/hide overlays on a base diagram.
Pedagogical use: dense diagrams where every annotation matters but all-at-once overwhelms.

```html
<fieldset class="widget">
  <legend>Show</legend>
  <label><input type="checkbox" data-layer="vec" checked> Force vectors</label>
  <label><input type="checkbox" data-layer="labels"> Axis labels</label>
  <svg width="300" height="200" viewBox="0 0 300 200">
    <rect x="100" y="80" width="100" height="40" fill="#ccc"/>
    <g data-layer="vec">
      <line x1="150" y1="100" x2="150" y2="40" stroke="var(--accent)" stroke-width="3"/>
    </g>
    <g data-layer="labels" hidden>
      <text x="10" y="100">y axis</text>
    </g>
  </svg>
</fieldset>
<script>
  document.querySelectorAll('[data-layer]').forEach(el => {
    if (el.tagName === 'INPUT')
      el.addEventListener('change', () =>
        document.querySelector(`g[data-layer="${el.dataset.layer}"]`).hidden = !el.checked);
  });
</script>
```

---

## 5. Inline Quiz with Diagnostic Feedback

What: multiple-choice where wrong answers each get a tailored explanation — not just "incorrect".
Pedagogical use: end of a section to lock the concept in. Wrong answers are *teaching moments*, not failures.

```html
<div class="quiz" data-correct="b">
  <p class="quiz-q">If we halve the learning rate, training will…</p>
  <button data-k="a">…always converge faster</button>
  <button data-k="b">…take more steps but be more stable</button>
  <button data-k="c">…always diverge</button>
  <p class="quiz-fb" data-fb="a" hidden>No — smaller steps mean <em>more</em> iterations, not fewer. You'd reach a similar minimum but more slowly.</p>
  <p class="quiz-fb correct" data-fb="b" hidden>Right. Stability up, wall-clock up. The trade-off you're making is exploration speed for reliability.</p>
  <p class="quiz-fb" data-fb="c" hidden>Divergence comes from too-LARGE rates, not too-small. Try the slider in section 2 to see this.</p>
</div>
<script>
  document.querySelectorAll('.quiz button').forEach(b => b.addEventListener('click', () => {
    const q = b.closest('.quiz');
    q.querySelectorAll('.quiz-fb').forEach(p => p.hidden = true);
    q.querySelector(`[data-fb="${b.dataset.k}"]`).hidden = false;
  }));
</script>
```

---

## 6. Before/After Comparison Slider

What: drag a divider between two states.
Pedagogical use: visualizing the *effect* of a single change (no-regularization vs L2, before/after refactor).

```html
<script type="module" src="https://cdn.jsdelivr.net/npm/img-comparison-slider@8/dist/index.js"></script>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/img-comparison-slider@8/dist/styles.css">
<img-comparison-slider>
  <img slot="first"  src="before.svg" alt="Without regularization"/>
  <img slot="second" src="after.svg"  alt="With L2 regularization"/>
</img-comparison-slider>
```

---

## 7. Scrollytelling (sticky graphic, scroll-driven morph)

What: as the reader scrolls past steps, a *sticky* graphic morphs. Uses `scrollama` (vanilla JS, ~5KB).
Pedagogical use: long-form narratives where the same diagram evolves through stages — NYT / Pudding style.

```html
<div class="scrolly">
  <div class="sticky-graphic" id="g">Step 0</div>
  <div class="step" data-step="1"><p>First insight: …</p></div>
  <div class="step" data-step="2"><p>Then this: …</p></div>
  <div class="step" data-step="3"><p>Finally: …</p></div>
</div>
<script>
  scrollama().setup({step: '.scrolly .step', offset: 0.5}).onStepEnter(({element}) => {
    document.getElementById('g').textContent = 'Step ' + element.dataset.step;
  });
</script>
```

Required CSS:
```css
.scrolly { position: relative; }
.sticky-graphic { position: sticky; top: 20vh; height: 60vh; }
.step { min-height: 60vh; padding: 20vh 0; }
```

---

## 8. "Why?" Disclosure (zero JS)

What: native `<details>` to hide deeper justification.
Pedagogical use: every leap an advanced reader could question. Beginners skip; experts click.

```html
<p>
  The optimum is the <strong>median</strong>, not the mean.
  <details>
    <summary>Why?</summary>
    Because minimizing Σ|x−c| has derivative sign(x−c), which sums to zero
    exactly when half the points are on each side — i.e., at the median.
  </details>
</p>
```

---

## 9. Live Code Playground (no deps)

What: editable code → re-runs on change. For a single file, plain `<textarea>` + `eval` in a sandboxed iframe.
Pedagogical use: teaching syntax, regex, SQL, small algorithms.

```html
<div class="playground">
  <textarea id="code" rows="6">[1,2,3].map(x => x*x).reduce((a,b) => a+b, 0)</textarea>
  <button id="run">Run</button>
  <pre id="out"></pre>
</div>
<script>
  document.getElementById('run').addEventListener('click', () => {
    try { document.getElementById('out').textContent = eval(document.getElementById('code').value); }
    catch (e) { document.getElementById('out').textContent = 'Error: ' + e.message; }
  });
</script>
```

For multi-language playgrounds, escalate to CodeMirror 6 (~300KB modular). Skip Monaco (5–10MB).

---

## 10. Concept Map — Highlights as You Read

What: a small SVG/Mermaid graph in a sidebar; IntersectionObserver highlights the node matching the current section.
Pedagogical use: explainers with 5–15 interlinked ideas. Reduces "where am I?" load.

```html
<nav class="concept-map">
  <ol>
    <li data-section="motivation">Motivation</li>
    <li data-section="setup">Setup</li>
    <li data-section="derivation">Derivation</li>
    <li data-section="example">Example</li>
    <li data-section="failure-modes">Failure modes</li>
  </ol>
</nav>
<script>
  const obs = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        document.querySelectorAll('.concept-map li').forEach(li => li.classList.remove('active'));
        document.querySelector(`.concept-map [data-section="${e.target.id}"]`)?.classList.add('active');
      }
    });
  }, {rootMargin: '-40% 0px -40% 0px'});
  document.querySelectorAll('article section[id]').forEach(s => obs.observe(s));
</script>
```

---

## 11. Tufte-Style Sidenotes (zero JS)

What: push asides into the margin instead of forcing a footnote jump.
Pedagogical use: tangential context, source citations, "here be dragons" warnings — anything the main flow can do without.

```html
<p>
  The result follows from the chain rule.
  <label for="sn-1" class="margin-toggle sidenote-number"></label>
  <input type="checkbox" id="sn-1" class="margin-toggle"/>
  <span class="sidenote">
    Specifically, ∂L/∂w = (∂L/∂y)(∂y/∂w), where the first factor is the upstream gradient.
  </span>
  Once you've internalized this, backprop stops feeling magical.
</p>
```

(Loads automatically when `tufte.css` is included.)

---

## 12. Color-Coded Variables (the 3Blue1Brown move)

What: wrap every instance of a symbol in a span with a matching CSS color. The same red `x` appears in prose, equation, and diagram.
Pedagogical use: link symbols across representations so the eye stitches them together.

```html
<p>
  We want to find <span class="var-x">x</span> that minimizes the distance
  between <span class="var-x">x</span> and the target <span class="var-y">y</span>.
</p>
<p>$\text{minimize} \quad \|\color{#c33}{x} - \color{#39c}{y}\|^2$</p>
```

CSS (in `lesson-base.css`):
```css
.var-x { color: #c33; font-weight: 600; }
.var-y { color: #39c; font-weight: 600; }
.var-z { color: #2a7; font-weight: 600; }
```

Always use the same hex in the LaTeX `\color{}` macro and the CSS — the eye must match them instantly.

---

## 13. KaTeX Math (loaded in template)

Inline: `$E = mc^2$` · Display: `$$\int_0^\infty e^{-x^2}\,dx = \frac{\sqrt{\pi}}{2}$$`

Color-code matching terms across prose and equation. Always wrap variable names mentioned in prose in the matching `.var-*` class.

---

## 14. Mermaid Diagrams (for flowcharts / sequence diagrams)

```html
<pre class="mermaid">
flowchart LR
  Input --> Embed
  Embed --> Attention
  Attention --> FFN
  FFN --> Output
</pre>
```

Loaded once per page via the template. Use only for flow / sequence / state / class diagrams. For everything else (function plots, vector fields, custom geometry) use hand-written SVG.

---

## 15. Anime.js Animation (timeline, stagger)

```html
<script type="module">
  import { animate, stagger } from 'https://cdn.jsdelivr.net/npm/animejs@4/lib/anime.esm.min.js';
  animate('.fade-in', {
    opacity: [0, 1],
    translateY: [20, 0],
    delay: stagger(80),
    duration: 600,
    easing: 'out-quad',
  });
</script>
```

90% of the time, CSS `@keyframes` is enough. Reach for anime.js only when you need timelines or stagger.

---

## 16. Reading-Progress Bar

```html
<div id="progress"></div>
<script>
  addEventListener('scroll', () => {
    progress.style.width = (scrollY / (document.body.scrollHeight - innerHeight) * 100) + '%';
  });
</script>
```

CSS:
```css
#progress {
  position: fixed; top: 0; left: 0;
  height: 3px; background: var(--accent);
  width: 0; z-index: 100;
  transition: width 80ms linear;
}
```

---

## 17. "Ask Claude" Clipboard Button — extend dialogue into Claude Code

What: a button that copies a pre-formed prompt to the clipboard, so the reader pastes it into Claude Code for a deeper explanation.
Pedagogical use: every section. The HTML is the textbook; Claude Code is the tutor sitting next to it. This is how "chatting with me" works in this skill.

```html
<button class="ask-claude" data-prompt="In the lesson on backpropagation, expand on the chain rule step with a worked numeric example using a 2-layer network.">
  💬 Ask Claude to go deeper
</button>
<script>
  document.querySelectorAll('.ask-claude').forEach(b => b.addEventListener('click', async () => {
    await navigator.clipboard.writeText(b.dataset.prompt);
    const orig = b.textContent;
    b.textContent = '✓ Copied — paste in Claude Code';
    setTimeout(() => b.textContent = orig, 2500);
  }));
</script>
```

**Place one at the end of every section.** Each prompt should be specific: reference the lesson title, the section name, and ask for a concrete extension (worked example, alternative analogy, counterexample, deeper proof). Vague "tell me more" prompts produce vague answers.

---

## 18. Common Wrong Intuition Callout

What: a styled callout naming a specific misconception readers usually have, and refuting it.
Pedagogical use: failure modes are where intuition lives. Every concept gets one.

```html
<aside class="wrong-intuition">
  <h4>⚠️ A common wrong intuition</h4>
  <p>
    "Larger learning rate = faster training." This is true up to a point —
    then the loss starts oscillating wildly and never converges. The sweet
    spot is "as large as you can make it without the loss bouncing."
  </p>
</aside>
```

---

## 19. ADEPT Concept Card

What: a single concept presented as Analogy → Diagram → Example → Plain English → Technical definition.
Pedagogical use: a standard format for introducing any new abstraction. Reduces ad-hoc decisions about how to structure each one.

```html
<article class="adept">
  <header><h3>Eigenvector</h3></header>
  <div class="adept-a">
    <strong>Analogy:</strong> Spinning a globe on its axis. The axis itself doesn't move while everything else does.
  </div>
  <div class="adept-d"><!-- SVG diagram of vector unchanged by transform --></div>
  <div class="adept-e"><strong>Example:</strong> For matrix [[2,0],[0,3]], the vector (1,0) is stretched to (2,0) — still pointing the same way.</div>
  <div class="adept-p"><strong>Plain English:</strong> A vector the matrix only stretches, never rotates.</div>
  <div class="adept-t"><strong>Technical:</strong> $v$ such that $Av = \lambda v$ for some scalar $\lambda$.</div>
</article>
```

---

## 20. Retrieval Prompts at Section End

What: 2–3 short questions the reader answers before scrolling further (Matuschak / mnemonic medium style).
Pedagogical use: spaced retrieval is the single most evidence-backed memory aid. End every section with these.

```html
<section class="retrieval">
  <h4>Before continuing…</h4>
  <ol>
    <li>In your own words, what does the learning rate control?</li>
    <li>What goes wrong if it's too big? Too small?</li>
    <li>Sketch (mentally) the loss curve for a learning rate that's just barely too high.</li>
  </ol>
</section>
```

---

## Starter Stack — Always Load

For maximum teaching power, minimum bloat (~50KB total over the wire, gzipped):

```html
<!-- Typography & Tufte-style sidenotes -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/edwardtufte/tufte-css@gh-pages/tufte.min.css">

<!-- Math (always) -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"
  onload="renderMathInElement(document.body, {delimiters: [{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}]})"></script>

<!-- Scrollytelling (load only if used) -->
<script defer src="https://cdn.jsdelivr.net/npm/scrollama@3.2.0/build/scrollama.min.js"></script>

<!-- Flow diagrams (load only if used) -->
<script type="module">
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
  mermaid.initialize({startOnLoad: true, theme: 'neutral'});
</script>

<!-- Animation (load only if used) -->
<!-- <script type="module">import {animate, stagger} from 'https://cdn.jsdelivr.net/npm/animejs@4/lib/anime.esm.min.js';</script> -->
```

**Hard defaults for every lesson:**
- Single file, no build, no `npm install`. Opens with `open lesson.html`.
- KaTeX (not MathJax). Tufte CSS (not Bootstrap). Vanilla SVG (not D3).
- Every concept gets either a slider, a predict-then-reveal, or a quiz — never three paragraphs in a row without interaction.
- Color the same variable the same way in prose, equation, and diagram.
- Every section ends with an "Ask Claude to go deeper" clipboard button and 2–3 retrieval prompts.
