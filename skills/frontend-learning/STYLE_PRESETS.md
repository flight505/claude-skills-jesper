# Style Presets — Visual Aesthetics for Lessons

Distinct aesthetics for lesson pages. Each preset is a CSS-variable override on top of `lesson-base.css`. Pick one (or show the user 2–3 small previews so they pick) — **never** invent a generic preset. The whole point is to avoid AI-slop.

**How to use:** include `lesson-base.css` inline, then override the `:root` variables and any extras shown below. Each preset notes when it fits.

---

## 1. Ciechanowski Warm — the default

**Vibe:** warm paper, serif body, precise geometry, lots of inline figures.
**Best for:** mechanical / physical concepts, anything benefiting from "I'm reading a careful craftsman's notebook."

```css
:root {
  --bg: #f5f1e8;
  --bg-card: #ffffff;
  --fg: #1f1d18;
  --accent: #b8430f;      /* burnt orange */
  --accent2: #2c5e7c;     /* dusty blue */
  --accent3: #5a7c2c;     /* moss */
  --border: #d4cdb8;
  --serif: et-book, Charter, "Iowan Old Style", "Palatino Linotype", Palatino, serif;
}
body { font-feature-settings: "kern", "liga", "onum"; }
h1, h2, h3 { font-family: var(--serif); font-style: italic; font-weight: 500; }
```

---

## 2. Distill Academic

**Vibe:** restrained, scholarly, lots of margin annotations, blue accents.
**Best for:** ML papers / theoretical concepts. The default if the source is an arxiv paper.

```css
:root {
  --bg: #ffffff;
  --bg-card: #fafafa;
  --fg: #2a2a2a;
  --accent: #1a4fa3;
  --accent2: #b03a48;
  --accent3: #2a7a5e;
  --border: #e6e6e6;
  --measure: 36em;
  --serif: "Source Serif Pro", "Source Serif 4", Georgia, serif;
  --sans: "Source Sans Pro", "Source Sans 3", -apple-system, sans-serif;
}
h1, h2, h3 { font-family: var(--sans); font-weight: 700; letter-spacing: -0.02em; }
.var-x { color: #b03a48; }
.var-y { color: #1a4fa3; }
```

---

## 3. 3Blue1Brown Dark

**Vibe:** dark background, vibrant blues/oranges, animation-forward.
**Best for:** math / linear algebra / calculus where colored vectors and animated transforms are the lesson.

```css
:root {
  --bg: #0e0f12;
  --bg-card: #1a1d22;
  --bg-callout: #1f1a0e;
  --bg-quiz: #0e1a25;
  --bg-predict: #1a1410;
  --bg-retrieval: #0e1a14;
  --bg-wrong: #1a0e0e;
  --fg: #e8e6e0;
  --muted: #8a8a90;
  --border: #2a2d34;
  --accent: #ffb86c;      /* 3b1b orange */
  --accent2: #6ab0e8;     /* 3b1b blue */
  --accent3: #b0d977;     /* 3b1b green */
  --serif: "Source Serif Pro", Georgia, serif;
  --sans: "Inter", -apple-system, sans-serif;
}
h1, h2, h3 { font-family: var(--sans); font-weight: 600; letter-spacing: -0.01em; }
body { font-family: var(--sans); }
```

---

## 4. Better Explained Friendly

**Vibe:** chatty, conversational, second-person, lots of inline analogies and asides.
**Best for:** "intuition-first" pieces where the analogy is the lesson (interest rates, prob theory, calculus first concepts).

```css
:root {
  --bg: #fefdfa;
  --bg-card: #ffffff;
  --fg: #2c2a26;
  --accent: #d97706;      /* warm amber */
  --accent2: #0891b2;     /* teal */
  --accent3: #65a30d;
  --border: #ede8da;
  --serif: "Charter", "Iowan Old Style", Georgia, serif;
  --sans: "Inter", "Segoe UI", sans-serif;
}
h1, h2, h3 { font-family: var(--sans); font-weight: 700; }
.socratic { font-style: italic; background: #fff8e1; padding: 0.75rem 1rem; border-radius: 4px; border-left: 3px solid var(--accent); }
```

---

## 5. Tufte Classical

**Vibe:** sidenotes everywhere, full-bleed figures, very long measure for prose.
**Best for:** topics with lots of tangential context, asides, or source notes — historical, data-viz, statistical.

```css
:root {
  --bg: #fffff8;
  --bg-card: #fffef0;
  --fg: #111;
  --accent: #8b1a1a;
  --accent2: #1a4a8b;
  --accent3: #4a7a1a;
  --border: #d8d4c0;
  --measure: 38em;
  --serif: et-book, "ET Book", Palatino, "Palatino Linotype", "Palatino LT STD", "Book Antiqua", Georgia, serif;
}
/* Tufte CSS handles most of this already — these mostly tweak accents */
```

---

## 6. Nicky Case Playful

**Vibe:** hand-drawn, friendly, cartoony comic-mono headers, bright primary colors.
**Best for:** social / behavioral / game-theory / systems-thinking — anywhere the "explorable game" framing wins.

```css
:root {
  --bg: #fff9ee;
  --bg-card: #ffffff;
  --fg: #1a1a1a;
  --accent: #ff5d6c;       /* coral pink */
  --accent2: #4ec5e9;      /* sky */
  --accent3: #ffd23f;      /* sun yellow */
  --border: #1a1a1a;
  --serif: "Patrick Hand", "Architects Daughter", Georgia, cursive;
  --sans: "Comic Neue", "Patrick Hand", "Trebuchet MS", sans-serif;
}
h1, h2, h3 { font-family: var(--serif); font-weight: 700; }
.widget, .predict, .quiz, .retrieval { border: 2px solid var(--border); box-shadow: 4px 4px 0 var(--border); }
button { border: 2px solid var(--border) !important; box-shadow: 3px 3px 0 var(--border); }
button:active { transform: translate(2px, 2px); box-shadow: 1px 1px 0 var(--border); }
```

---

## 7. Quantum Country Mnemonic

**Vibe:** minimal, lots of inline spaced-repetition prompts, mostly-white, careful typography.
**Best for:** memory-heavy topics (vocabulary, formulas you need to recall, language grammar).

```css
:root {
  --bg: #ffffff;
  --bg-card: #f8f8f8;
  --fg: #1a1a1a;
  --accent: #1e8a3c;       /* memory green */
  --accent2: #5b4dc4;
  --accent3: #c14b1a;
  --border: #e8e8e8;
  --measure: 34em;
  --serif: "Charter", "Iowan Old Style", Georgia, serif;
  --sans: "Inter", -apple-system, sans-serif;
}
.retrieval { background: #f0f7ed; }
/* Quantum Country style: prompts inline every ~3 paragraphs, not just at end */
```

---

## 8. Acko Typographic

**Vibe:** typography IS the design. Almost no chrome. Big type, tight grid.
**Best for:** essays-as-lesson, philosophy-of-X pieces, single-idea deep dives where the writing carries the weight.

```css
:root {
  --bg: #ffffff;
  --bg-card: #f8f8f8;
  --fg: #1a1a1a;
  --accent: #c41e3a;
  --accent2: #1a1a1a;
  --accent3: #5a5a5a;
  --border: transparent;
  --measure: 32em;
  --serif: "Crimson Pro", "Crimson Text", "Iowan Old Style", Georgia, serif;
}
body { font-size: 1.2rem; line-height: 1.7; }
h1 { font-size: 3.5rem; font-weight: 700; letter-spacing: -0.04em; line-height: 1; margin-bottom: 2rem; }
h2 { font-weight: 400; font-style: italic; }
.widget { background: transparent; border: none; padding: 0; }
```

---

## How to Pick a Preset

If the user names a topic, infer a sensible default — but **show 2–3 preview swatches** and let them pick. A swatch is just an H1 + a few sentences + one widget rendered in the candidate preset. Use the [Visual Style Discovery] phase in SKILL.md.

Quick mappings:
- ML paper / theoretical → Distill or 3Blue1Brown Dark
- Physics / mechanical / how-things-work → Ciechanowski
- First-contact intuition / analogies-heavy → Better Explained
- Lots of asides / historical / annotated → Tufte
- Social / behavioral / explorable game → Nicky Case
- Vocab / formula recall → Quantum Country
- Single-essay deep dive → Acko
- Math / linear algebra with colored vectors → 3Blue1Brown Dark

**Never invent a new preset on the fly** — pick from these or extend one. Inventing presets is how you slip into generic AI slop.
