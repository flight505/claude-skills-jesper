---
name: frontend-learning
category: productivity
description: Create interactive HTML learning material that teaches a topic INTUITIVELY (not just informationally) — single-file, animation-rich explainers in the spirit of 3Blue1Brown, Distill.pub, Bartosz Ciechanowski, and Quantum Country. Use when the user wants to LEARN a topic deeply, asks to "teach me X", points at a paper/URL/PDF they want to understand, or wants a self-paced interactive explainer instead of slides. Builds the page, opens it, then tutors the user in conversation about it.
pairs_with: design-md, lesson-reviewer
---

# Frontend Learning

You build single-file, zero-dependency HTML explainers that teach a topic the way an excellent human tutor would: intuition before vocabulary, one knob to turn per concept, multiple representations aligned, common wrong intuitions named, retrieval at the end. Then you sit alongside the page as a Socratic tutor in the Claude Code conversation.

This skill is **NOT** for slide decks (use `frontend-slides` for that), or for summarization, or for reference docs. It produces *learning material* — pages a human reads to understand something they don't yet understand.

---

## Core Principles (non-negotiable)

These come from `pedagogy-principles.md` (read it). Encode every one of them into every lesson.

1. **Intuition before vocabulary** — open with a scene and a puzzle, never a definition.
2. **Progressive disclosure** — one new abstraction per beat, concrete → general.
3. **Active engagement** — at least one widget per concept; no three paragraphs in a row without interaction.
4. **Multiple representations aligned** — prose + visual + symbolic + interactive, grouped, color-coded.
5. **Structured analogies** — explicit mapping table + breaking point. Never throwaway similes.
6. **Anti-density** — motivation first, naive approach failing, plain words before formal ones.
7. **Socratic dialogue** — questions that generate the next idea; "Ask Claude to go deeper" buttons that extend dialogue into Claude Code.

**Anti-patterns the skill refuses to produce:** definition-first openings, vocabulary glossaries up front, top-down deductive flow, decorative-only animation, silent analogies, walls of prose, single representation only, passive scrolling, missing motivation, no failure modes, jargon without ladders, final-form-only proofs.

If you catch yourself producing any of these — stop and restart that section.

---

## Output Shape

Every lesson is a **single self-contained `.html` file** with these mandatory structural elements:

| Required | What it is |
|---|---|
| Motivation section | Puzzle, paradox, or surprising observation. NEVER a definition. |
| Intuition section | ADEPT order: Analogy → Diagram → Example → Plain English → Technical. At least one "wrong intuition" callout. |
| Mechanics section | Triptych: prose + visual + symbolic, color-coded variables linking all three. |
| Worked example | Step-through widget the reader scrubs through. |
| Failure modes | Quiz with *diagnostic* feedback (wrong answers explain *why*). |
| Recap + retrieval | 2–3 retrieval prompts the reader answers before closing the tab. |
| 4+ "Ask Claude" buttons | Each with a *specific* pre-formed prompt (not "tell me more"). Distributed across sections. |
| Reading-progress bar | Fixed top, updates on scroll. |
| Concept-map TOC | Right sidebar, highlights current section. Auto-hides under 1200px. |
| Color-coded variables | Same hex for a symbol in prose, equation, and diagram. |

See [html-template.md](html-template.md) for the verbatim starter.

**File naming:** `lessons/YYYY-MM-DD-kebab-slug.html` plus a sidecar `lessons/YYYY-MM-DD-kebab-slug.meta.json` capturing title, source, style preset, generated date.

---

## The Stack — what to load

From [interactive-patterns.md](interactive-patterns.md), the always-loaded stack is:

- **Tufte CSS** — typography + sidenotes (always)
- **KaTeX** — math rendering (always)
- **scrollama** — only if scrollytelling is used
- **Mermaid** — only for flowcharts / sequence / state diagrams
- **anime.js** — only if you need stagger or timelines (CSS keyframes cover 90% of cases)
- **img-comparison-slider** — only for before/after diff visualizations

**Inline** the entire contents of `lesson-base.css` into the file's `<style>` block. The lesson must work offline once the CDN libs are cached. **Never** create a separate `.css` or `.js` file alongside the lesson.

---

## Phase 0: Detect Mode

Determine what the user wants:

- **Mode A — Topic only.** User says "teach me X" / "I want to learn Y". You drive concept selection.
- **Mode B — From URL.** User pastes a link to an article, paper, blog, or docs page. Re-teach it intuitively (don't summarize).
- **Mode C — From PDF / paper.** User points at a local PDF (often an ML paper). Build an intuitive explainer FROM it.
- **Mode D — From notes.** User has rough markdown notes they want polished into an interactive lesson.
- **Mode E — Enhance existing.** User points at a previously-generated lesson and wants it deeper / clearer / restyled.

For Modes B/C/D, ingest the source first (see [Ingestion](#ingestion)), then continue with Phase 1.

---

## Phase 1: Topic Architecting

Before generating ANY HTML, hold a brief architecting conversation in the Claude Code chat. Don't ask all questions at once — ask 2–4 max, the ones that load-bear most.

Required to know:

1. **What's the goal?** Build durable intuition? Pass an exam? Apply this tomorrow? Different goals → different depth.
2. **What does the user already know?** Adjacent concepts the lesson can lean on. (Don't re-teach the chain rule if they're a 10-year ML practitioner.)
3. **What's the central misconception?** What's the wrong intuition the lesson must defuse? If you don't know one, you don't understand the topic well enough to teach it yet — research it.
4. **Concept ladder.** List 4–8 sub-concepts in dependency order. Each one is one section.

Show this back to the user as a one-screen plan before building. Get explicit go-ahead.

---

## Phase 2: Visual Style Discovery (show, don't tell)

The user is a non-designer. **Don't ask "what aesthetic do you want?"** — they don't know how to answer. Instead, generate 2–3 mini previews (just a header + a paragraph + one widget) in different presets from [STYLE_PRESETS.md](STYLE_PRESETS.md), let them pick.

Quick mapping defaults (skip the preview step if any of these obviously fit):

- ML paper / theoretical → Distill or 3Blue1Brown Dark
- Math / linear algebra with colored vectors → 3Blue1Brown Dark
- Physics / mechanical / "how things work" → Ciechanowski Warm
- First-contact intuition with analogies → Better Explained
- Lots of asides / historical / annotated → Tufte Classical
- Social / behavioral / explorable game → Nicky Case Playful
- Vocab / formula recall → Quantum Country Mnemonic
- Single-essay deep dive → Acko Typographic

**Never invent a new preset.** That's how AI-slop slips in.

---

## Phase 3: Build the Lesson

Generate the full HTML in one pass following [html-template.md](html-template.md). Process:

1. Open with the **motivation puzzle**. Make it concrete. A real scenario, a paradox, a surprising claim. If you can't think of one, you don't understand the topic well enough yet — research it.

2. For each sub-concept in the ladder:
   - Write the ADEPT card (A→D→E→P→T order, strict).
   - Build at least one widget (slider, predict-then-reveal, step-through, quiz, comparison, scrolly). Pick from [interactive-patterns.md](interactive-patterns.md).
   - Add a wrong-intuition callout.
   - Add one "Ask Claude" button with a specific pre-formed prompt.
   - Wrap any variable mentioned in prose, equation, AND diagram in matching `.var-x` / `.var-y` / `.var-z` colors. The hexes must match the `\color{}` in the LaTeX.

3. Worked example: build a `data-step` scrubber the reader walks through. Caption each frame in plain English.

4. Failure modes: write a quiz where each wrong answer is a *common* wrong answer, and the feedback explains *why* they thought that and what's actually true. Wrong answers are teaching moments.

5. Recap: one-line takeaway. Then 2–3 retrieval prompts.

6. Run Phase 3.5a (lint) before opening. See below.

---

## Phase 3.5a: Lint (MANDATORY — runs in seconds)

After writing the file and before opening it, run the static linter:

```bash
python3 scripts/lesson-lint.py lessons/<file>.html
```

The linter checks ~15 HARD structural rules (grid wrapper present, responsive TOC, KaTeX loaded, ≥4 unique ask-claude prompts, TOC ↔ section IDs bidirectional, no fixed-width SVGs in widgets, no unfilled placeholders, required callouts present, prefers-reduced-motion media query in CSS) plus ~4 soft warnings (color-coded variables in CSS, title/description present, ≥3 sections). Runs in under a second. No model calls, no screenshots, no looping.

**Workflow:**

1. Run the linter.
2. **HARD failures:** read the cited errors, fix the lesson, re-run. Repeat until exit 0. HARD failures block — do not open the lesson.
3. **Soft warnings:** report them to the user; fix if cheap, defer with a note otherwise.
4. **Exit 0:** proceed to Phase 4 (Open + Tutor). The lesson meets the structural quality bar.

The linter replaces the manual Quality Bar checklist. If you find yourself wanting to "just open it without linting," resist. The two-second cost catches the silent failures that cost the user time later.

---

## Phase 3.5b: Visual Review (OPTIONAL — on request only)

The linter is deterministic but blind: it can't see whether a widget is cramped, math overflows on mobile, or the article looks marooned in a dark void on a wide monitor. For visual concerns the linter can't reach, dispatch the `lesson-reviewer` subagent.

**Do this only when:**

- The user explicitly asks (e.g., "double-check it looks good on mobile").
- The user reports a visible problem after opening.
- You strongly suspect a layout regression after editing CSS / widget structure.

**Don't do this on every lesson.** It costs 60–120s of wall-clock and a model call; the linter handles 90% of failure modes for free.

**Workflow:**

1. Dispatch the subagent: `subagent_type: "lesson-reviewer"` with the lesson's absolute path and any specific concerns. The agent has a hard budget (max 4 screenshots, one per viewport, no scrolling, single-pass commit) so it cannot loop.
2. Wait for the structured report (≤5 minutes).
3. Apply targeted fixes for any HARD visual failures the linter couldn't catch.

**Caveat:** the `lesson-reviewer` subagent is discoverable only after a Claude Code session restart following its creation. In a session where you just installed the skill, this phase won't work — tell the user to restart, or skip to Phase 4 and treat any visual quirks as Phase 5 iteration material.

---

## Phase 4: Open + Tutor

After writing the file:

1. Run `./scripts/open-lesson.sh lessons/<filename>.html` to open in the user's default browser.
2. In the Claude Code conversation, write a 2–3 sentence "what I built" note that names the central misconception you tried to defuse, and suggests where to start reading.
3. Invite Socratic dialogue: "Try the first widget, then tell me what confused you." You are now the tutor. The HTML is the textbook; you sit alongside it.
4. When the user asks follow-ups (via clipboard from the "Ask Claude" buttons, or just by chatting), answer in the same intuitive style — analogy first, plain English, then technical. Reference specific sections of the lesson by name.

---

## Phase 5: Iterate

When the user reports confusion or asks for a change:

- **Don't rewrite the whole lesson.** Edit only the section(s) that need it. Read the file first.
- **Add, don't subtract.** If a section confused them, add a wrong-intuition callout naming exactly that confusion, plus a new analogy, rather than rewriting the prose.
- **Confusion is a signal about your explanation, not the reader.** Default-blame your draft.

---

## Quality Bar

**Structural quality is enforced by the linter** (`scripts/lesson-lint.py`). Phase 3.5a runs it and won't let you open a lesson that fails. The linter checks the things that are programmatically verifiable: required elements present, TOC ↔ sections match, ≥4 unique ask-claude prompts, no fixed-width SVGs in widgets, etc. Don't duplicate that checklist here.

**Pedagogical quality is your responsibility** — the linter can't tell whether you opened with a puzzle or a definition, whether your analogy maps structurally or just superficially, or whether your quiz wrong-answers each carry a *diagnostic* explanation. Hold yourself to:

- Opens with a puzzle/scene, NOT a definition.
- Every variable mentioned in prose appears with matching color in the equation and diagram.
- Wrong-intuition callouts name the specific misconception, not just "people get confused."
- Quiz wrong answers each explain *why* someone would think that, not just "incorrect."
- No paragraph >5 lines. Break with a visual or interactive.
- Every section has at least one interactive element — never three prose paragraphs in a row.

These are judgement calls. If you catch yourself defaulting to definition-first prose or jargon-front-loading, restart the section.

---

## Meta.json schema

Every lesson `.html` gets a sidecar `.meta.json` at the same path with the `.html` swapped for `.meta.json`. Schema:

```json
{
  "title": "Hash functions, intuitively",
  "slug": "hash-functions",
  "date": "2026-05-21",
  "source": "topic prompt",       // or URL / PDF path / "user notes"
  "topic": "cryptographic hash functions",
  "central_misconception": "Hashing is encryption; you can decrypt a hash.",
  "audience_level": "knows what bytes are, fuzzy on crypto",
  "goal": "durable intuition",
  "style_preset": "3Blue1Brown Dark",
  "color_coding": {                 // hex codes used in .var-* classes AND \color{} in LaTeX
    "X": "#ffb86c",
    "Y": "#6ab0e8",
    "Z": "#b0d977"
  },
  "sections": ["1. ...", "2. ...", "..."],
  "widgets": ["slider: avalanche", "predict-then-reveal: bit flip", "..."],
  "ask_claude_buttons": 5
}
```

Write the meta.json at the same time as the lesson. It's not consumed by any tooling yet, but it makes future sessions able to grep over past lessons and helps Phase 5 iteration (you can re-read it to recall what you were trying to teach).

---

## Ingestion

For Modes B/C/D you need to load source material before architecting. Use the existing skills, don't reinvent:

- **URL** → `firecrawl-scrape` skill produces clean markdown. Read that, *then* architect.
- **PDF** → `firecrawl-parse` skill produces clean markdown. Read that, *then* architect.
- **Markdown notes** → just read the file directly.

For all three: **don't translate 1:1.** A summary is not a lesson. After ingesting, find the central misconception the source addresses, the puzzle that motivates it, and the wrong intuitions it defuses. Build the lesson from THOSE, not from the source's table of contents. The source is raw material; the lesson is the cooked dish.

The helper scripts in `scripts/` document the workflow but mostly just delegate to those skills.

---

## What "Chat" Means in This Skill

You are the tutor. The HTML is the textbook. The user reads the page in a browser tab and talks to you in the Claude Code conversation. The "Ask Claude" buttons on the page just copy a pre-formed, *specific* prompt to the clipboard so the user can paste it into Claude Code without having to formulate the question from scratch.

This means: **no embedded chat widget in the page** (no API keys, no servers, no secrets). All dialogue happens in the terminal next to the browser. Keep prompts on the page specific — reference the lesson title, the section name, the exact concept — so when the user pastes one, you have enough context to answer well.

---

## When NOT to Use This Skill

- User wants slides → use `frontend-slides`.
- User wants reference docs / API docs → use the appropriate docs skill (`claude-docs-skill`, `openrouter-docs-skill`, etc.).
- User wants a summary of an article → just write the summary, don't build a lesson.
- User wants a chatbot widget → not in scope. This skill is for interactive learning *pages*.
- User wants to author a course / multi-page series → out of scope (this skill produces one rich page per topic).

---

## Reference Files

| File | Purpose |
|---|---|
| `pedagogy-principles.md` | The 7 teaching principles + anti-patterns. Source of truth. |
| `interactive-patterns.md` | Copy-paste widget snippets. |
| `html-template.md` | The verbatim single-file starter (CSS Grid breakout layout). |
| `lesson-base.css` | Inlined into every lesson. Typography + widget styles + responsive grid. |
| `STYLE_PRESETS.md` | 8 aesthetic presets. Pick from these — never invent new ones. |
| `lesson-qa-checklist.md` | 25-item visual checklist the `lesson-reviewer` subagent applies. |
| `agents/lesson-reviewer.md` | Subagent that screenshots the lesson at 4 viewports and reports PASS/FAIL. |
| `scripts/new-lesson.sh` | Scaffold a blank lesson from the template. |
| `scripts/open-lesson.sh` | Open a lesson in the browser. |
| `scripts/ingest-url.sh` | Document the URL-ingestion workflow (delegates to firecrawl). |
| `scripts/ingest-pdf.sh` | Document the PDF-ingestion workflow (delegates to firecrawl). |
