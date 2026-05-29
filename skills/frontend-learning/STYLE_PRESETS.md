# Style Presets — Visual Aesthetics for Lessons

Distinct aesthetics for lesson pages. Each preset is a CSS-variable override on top of `lesson-base.css`. Pick one (or show the user 2–3 small previews so they pick) — **never** invent a generic preset. The whole point is to avoid AI-slop.

**How to use:** include `lesson-base.css` inline, then override the `:root` variables and any extras shown below. Each preset notes when it fits.

**Evidence-based typography floor (applied to every preset):**
- Body: ≥ 17 px, line-height 1.60–1.65 (18 px / 1.65 for dark-mode presets)
- Measure: max 36 em (≈ 65–72 chars) — never 38 em or wider
- Headings: negative letter-spacing −0.02 em to −0.04 em; line-height 0.95–1.15
- Code / mono: JetBrains Mono on all presets (added to `--mono`)
- Source: Piepenbrock 2013, WCAG 1.4.8 AAA, Quantum Country / Distill audits

---

## 1. Ciechanowski Warm — the default

**Vibe:** warm paper, serif body, precise geometry, lots of inline figures.
**Best for:** mechanical / physical concepts, anything benefiting from "I'm reading a careful craftsman's notebook."

```css
:root {
  --bg:      #f5f1e8;
  --bg-card: #ffffff;
  --fg:      #1f1d18;          /* warm near-black — not pure #000 */
  --muted:   #6b6860;
  --accent:  #b8430f;          /* burnt orange */
  --accent2: #2c5e7c;          /* dusty blue */
  --accent3: #5a7c2c;          /* moss */
  --border:  #d4cdb8;
  --serif:   et-book, Charter, "Iowan Old Style", "Palatino Linotype", Palatino, serif;
  --mono:    "JetBrains Mono", ui-monospace, monospace;
}
body {
  font-family: var(--serif);
  font-size: 17px;
  line-height: 1.62;
  font-feature-settings: "kern", "liga", "onum";
}
h1, h2, h3 {
  font-family: var(--serif);
  font-style: italic;
  font-weight: 500;
  letter-spacing: -0.02em;
  line-height: 1.1;
}
```

---

## 2. Distill Academic

**Vibe:** restrained, scholarly, lots of margin annotations, blue accents.
**Best for:** ML papers / theoretical concepts. The default if the source is an arxiv paper.

```css
:root {
  --bg:      #ffffff;
  --bg-card: #fafafa;
  --fg:      #2a2a2a;
  --muted:   #6b6b6b;
  --accent:  #1a4fa3;
  --accent2: #b03a48;
  --accent3: #2a7a5e;
  --border:  #e6e6e6;
  --measure: 36em;
  --serif:   "Source Serif Pro", "Source Serif 4", Georgia, serif;
  --sans:    "Source Sans Pro", "Source Sans 3", -apple-system, sans-serif;
  --mono:    "JetBrains Mono", ui-monospace, monospace;
}
body {
  font-family: var(--serif);
  font-size: 17px;
  line-height: 1.62;
}
h1, h2, h3 {
  font-family: var(--sans);
  font-weight: 700;
  letter-spacing: -0.025em;
  line-height: 1.1;
}
.var-x { color: #b03a48; }
.var-y { color: #1a4fa3; }
```

---

## 3. 3Blue1Brown Dark

**Vibe:** dark canvas, vibrant blues/oranges, animation-forward, colored-vector-centric.
**Best for:** math / linear algebra / speech architectures where colored variables and animated transforms are the lesson. The three Series A lessons use this.

> **Scope note:** 3B1B Dark is justified when the primary information channel is the *animation* — colored vectors on a dark field. For prose-heavy lessons, a light preset is empirically better for comprehension. Default to this for math/ML architecture content; consider Distill or Ciechanowski for essay-style explanations.

```css
:root {
  --bg:           #0e0f12;
  --bg-card:      #1a1d22;
  --bg-callout:   #1f1a0e;
  --bg-quiz:      #0e1a25;
  --bg-predict:   #1a1410;
  --bg-retrieval: #0e1a14;
  --bg-wrong:     #1a0e0e;
  --fg:           #e8e6e0;
  --muted:        #8a8a90;
  --border:       #2a2d34;
  --accent:       #ffb86c;     /* 3b1b orange */
  --accent2:      #6ab0e8;     /* 3b1b blue */
  --accent3:      #b0d977;     /* 3b1b green */
  --serif:        "Source Serif Pro", Georgia, serif;
  --sans:         "Inter", -apple-system, sans-serif;
  --mono:         "JetBrains Mono", ui-monospace, monospace;
}
body {
  font-family: var(--sans);
  font-size: 18px;             /* larger than light mode — dark needs compensating */
  line-height: 1.65;
}
h1, h2, h3 {
  font-family: var(--sans);
  font-weight: 600;
  letter-spacing: -0.02em;
  line-height: 1.05;
}
```

---

## 4. Better Explained Friendly

**Vibe:** chatty, conversational, second-person, lots of inline analogies and asides.
**Best for:** "intuition-first" pieces where the analogy is the lesson — interest rates, probability theory, calculus first concepts.

```css
:root {
  --bg:      #fefdfa;
  --bg-card: #ffffff;
  --fg:      #2c2a26;          /* warm near-black — not pure #000 */
  --muted:   #6b6760;
  --accent:  #d97706;          /* warm amber */
  --accent2: #0891b2;          /* teal */
  --accent3: #65a30d;
  --border:  #ede8da;
  --serif:   "Charter", "Iowan Old Style", Georgia, serif;
  --sans:    "Inter", "Segoe UI", sans-serif;
  --mono:    "JetBrains Mono", ui-monospace, monospace;
}
body {
  font-family: var(--serif);
  font-size: 17px;
  line-height: 1.62;
}
h1, h2, h3 {
  font-family: var(--sans);
  font-weight: 700;
  letter-spacing: -0.025em;
}
.socratic {
  font-style: italic;
  background: #fff8e1;
  padding: 0.75rem 1rem;
  border-radius: 4px;
  border-left: 3px solid var(--accent);
}
```

---

## 5. Tufte Classical

**Vibe:** sidenotes everywhere, full-bleed figures, long-form prose rhythm.
**Best for:** topics with lots of tangential context, asides, or source notes — historical, data-viz, statistical.

> **Measure note:** 36 em ≈ 66–70 chars/line — the top of the evidence-based safe range. Do not widen past 36 em; wider triggers line-tracking errors at scale.

```css
:root {
  --bg:      #fffff8;
  --bg-card: #fffef0;
  --fg:      #111111;
  --muted:   #555550;
  --accent:  #8b1a1a;
  --accent2: #1a4a8b;
  --accent3: #4a7a1a;
  --border:  #d8d4c0;
  --measure: 36em;             /* FIXED from 38em — 38em overflows the safe CPL range */
  --serif:   et-book, "ET Book", Palatino, "Palatino Linotype", "Palatino LT STD", "Book Antiqua", Georgia, serif;
  --mono:    "JetBrains Mono", ui-monospace, monospace;
}
body {
  font-family: var(--serif);
  font-size: 17px;
  line-height: 1.62;
}
h1, h2, h3 {
  font-family: var(--serif);
  font-weight: 600;
  letter-spacing: -0.015em;
}
/* Tufte CSS handles sidenotes and margin-note layout — these tweak accents only */
```

---

## 6. Nicky Case Playful

**Vibe:** hand-drawn, friendly, cartoony comic-mono headers, bright primary colors.
**Best for:** social / behavioral / game-theory / systems-thinking — anywhere the "explorable game" framing wins.

```css
:root {
  --bg:      #fff9ee;
  --bg-card: #ffffff;
  --fg:      #1a1a1a;
  --muted:   #5a5a5a;
  --accent:  #ff5d6c;          /* coral pink */
  --accent2: #4ec5e9;          /* sky */
  --accent3: #ffd23f;          /* sun yellow */
  --border:  #1a1a1a;
  --serif:   "Patrick Hand", "Architects Daughter", Georgia, cursive;
  --sans:    "Comic Neue", "Patrick Hand", "Trebuchet MS", sans-serif;
  --mono:    "JetBrains Mono", ui-monospace, monospace;
}
body {
  font-family: var(--sans);
  font-size: 16px;             /* slightly smaller — matches the playful, light voice */
  line-height: 1.55;
}
h1, h2, h3 {
  font-family: var(--serif);
  font-weight: 700;
  letter-spacing: 0;           /* no negative tracking — the hand-drawn voice wants natural spacing */
}
.widget, .predict, .quiz, .retrieval {
  border: 2px solid var(--border);
  box-shadow: 4px 4px 0 var(--border);
}
button {
  border: 2px solid var(--border) !important;
  box-shadow: 3px 3px 0 var(--border);
}
button:active { transform: translate(2px, 2px); box-shadow: 1px 1px 0 var(--border); }
```

---

## 7. Quantum Country Mnemonic

**Vibe:** minimal, lots of inline spaced-repetition prompts, mostly-white, careful typography.
**Best for:** memory-heavy topics — vocabulary, formulas you need to recall, language grammar.

```css
:root {
  --bg:           #ffffff;
  --bg-card:      #f8f8f8;
  --bg-retrieval: #eef7ea;     /* slightly warmer green than #f0f7ed — retrieval gets a distinct home */
  --fg:           #1a1a1a;
  --muted:        #636363;
  --accent:       #1e8a3c;     /* memory green */
  --accent2:      #5b4dc4;
  --accent3:      #c14b1a;
  --border:       #e8e8e8;
  --measure:      34em;
  --serif:        "Charter", "Iowan Old Style", Georgia, serif;
  --sans:         "Inter", -apple-system, sans-serif;
  --mono:         "JetBrains Mono", ui-monospace, monospace;
}
body {
  font-family: var(--serif);
  font-size: 17px;
  line-height: 1.65;           /* slightly more open — retrieval prompts need visual breathing room */
}
h1, h2, h3 {
  font-family: var(--sans);
  font-weight: 600;
  letter-spacing: -0.02em;
}
.retrieval { background: var(--bg-retrieval); }
/* Quantum Country style: retrieval prompts inline every ~3 paragraphs, not just at end */
```

---

## 8. Acko Typographic

**Vibe:** typography IS the design. Almost no chrome. Big type, tight grid.
**Best for:** essays-as-lesson, philosophy-of-X pieces, single-idea deep dives where the writing carries the weight.

```css
:root {
  --bg:      #ffffff;
  --bg-card: #f8f8f8;
  --fg:      #1a1a1a;
  --muted:   #555555;
  --accent:  #c41e3a;
  --accent2: #1a1a1a;
  --accent3: #5a5a5a;
  --border:  transparent;
  --measure: 32em;
  --serif:   "Crimson Pro", "Crimson Text", "Iowan Old Style", Georgia, serif;
  --mono:    "JetBrains Mono", ui-monospace, monospace;
}
body {
  font-family: var(--serif);
  font-size: 19px;             /* essay format — slightly larger for sustained reading */
  line-height: 1.70;
}
h1 {
  font-size: 3.5rem;
  font-weight: 700;
  letter-spacing: -0.04em;
  line-height: 0.95;
  margin-bottom: 2rem;
}
h2 {
  font-family: var(--serif);
  font-weight: 400;
  font-style: italic;
  letter-spacing: -0.01em;
}
.widget { background: transparent; border: none; padding: 0; }
```

---

## How to Pick a Preset

If the user names a topic, infer a sensible default — but **show 2–3 preview swatches** and let them pick. A swatch is just an H1 + a few sentences + one widget rendered in the candidate preset. Use the [Visual Style Discovery] phase in SKILL.md.

Quick mappings:
- ML paper / theoretical → Distill or 3Blue1Brown Dark
- Speech / audio / ML architecture with colored variables → 3Blue1Brown Dark
- Physics / mechanical / how-things-work → Ciechanowski Warm
- First-contact intuition / analogies-heavy → Better Explained Friendly
- Lots of asides / historical / annotated → Tufte Classical
- Social / behavioral / explorable game → Nicky Case Playful
- Vocab / formula recall → Quantum Country Mnemonic
- Single-essay deep dive → Acko Typographic
- Ultrathink brand / YouTube course companion → *(see Ultrathink preset — in progress)*

**Never invent a new preset on the fly** — pick from these or extend one. Inventing presets is how you slip into generic AI slop.

### Dark mode guidance

Only 3Blue1Brown Dark and the forthcoming Ultrathink preset use a dark canvas. Dark mode is empirically *worse* for comprehension in prose-heavy content (Piepenbrock 2013, Dobres 2017). Use a dark preset only when:
- The primary information channel is an animated diagram with colored variables (3B1B Dark is optimized for exactly this)
- The brand context explicitly demands it (Ultrathink for course companion pages)

For all other topics, default to a light preset.
