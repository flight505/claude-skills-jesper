# Pedagogy Principles — How to Teach a Human Intuitively

These are the non-negotiable rules every lesson must follow. They come from cognitive load theory, dual coding, explorable explanations, the mnemonic medium, and the explanation philosophies of Feynman, Sanderson (3Blue1Brown), Victor, Case, and Matuschak.

**One-line encoding:** *Open with a scene and a question, hand the reader a knob to turn, show the answer in three aligned representations, name the failure mode, then ask them to retrieve it back.*

---

## 1. Mental-Model Formation — Build intuition BEFORE vocabulary

**Rule:** The reader must be able to *picture* and *predict* what the system does before you name any of its parts. Definitions are an *ending* point, not a starting point.

| DO | DON'T |
|---|---|
| Open with a concrete, manipulable scenario ("Imagine a ball rolling on a hilly surface. Where does it stop?"). Let the reader form a prediction. Then name the formal concept. | Open with a formal definition ("Gradient descent is an iterative first-order optimization algorithm…") and only later show a picture. |

**What this looks like in the HTML:** Every section opens with a *scene* — a labeled diagram, a one-sentence physical situation, or a tiny live demo. Never a definition box. The definition appears as a callout AFTER the reader has handled the idea.

---

## 2. Progressive Disclosure — Climb the ladder of abstraction

**Rule:** Sequence ideas concrete → general, specific instance → pattern → abstraction. New ideas depend only on ideas already shown on-screen. Introduce at most one new abstraction per beat.

| DO | DON'T |
|---|---|
| Show one worked example. Then two more. Then ask "what's the pattern?" Then name the pattern. Then generalize. | Present the general theorem and then "instantiate" it with examples — that's logical order, not pedagogical order. |

**What this looks like:** Sections are short (3–6 paragraphs). Each ends with a question the current section creates but doesn't answer — the hook into the next section. A visible "you are here" progress indicator or chapter ladder is always present.

---

## 3. Active Engagement — Reader does something every screen

**Rule:** Passive reading is forgotten; generation and retrieval are remembered. Every concept should be touchable — a slider, a "predict then reveal," a draggable handle, a fill-in, a click-to-step animation.

| DO | DON'T |
|---|---|
| Before revealing an answer, ask the reader to predict ("Drag the slider — what do you think happens when k > 1?"). Embed a tiny quiz prompt every 200–400 words. | Add interactivity that doesn't change anything explanatory. "Click to continue" with no choice is decoration, not engagement. Don't animate for animation's sake — every motion must carry meaning. |

**What this looks like:** At minimum one interactive widget per major concept, plus an inline "Check yourself" prompt after each section. Predict-then-reveal blocks render as a question with a hidden answer that uncovers on click.

---

## 4. Multiple Representations — Verbal + visual + symbolic + interactive, aligned

**Rule:** Dual coding theory: words and pictures stored in separate channels reinforce each other. Place words *next to* the visual they describe (spatial contiguity), present them *at the same time* (temporal contiguity), don't duplicate narration as on-screen text (redundancy principle).

| DO | DON'T |
|---|---|
| When introducing a formula, render it next to a labeled diagram and an interactive demo where the same variables are visibly named. Label parts of the picture with the exact same word used in the prose. | Put the equation on one page, the diagram on the next, the example three scrolls later. Use jargon in the caption that doesn't appear in the diagram. |

**What this looks like:** A repeating "triptych" pattern per concept — (1) plain-English sentence, (2) labeled visual or interactive, (3) symbolic / code form — visually grouped in one card, never split across scroll boundaries.

---

## 5. Analogies — Match structure, not surface; show where it breaks

**Rule:** Analogies work when *relational structure* maps, not when surface features match. Novices retrieve on surface similarity, so a good analogy must explicitly highlight the structural mapping AND its breaking point.

| DO | DON'T |
|---|---|
| Pick an analogy whose relational structure maps cleanly. State the mapping explicitly: "X here ↔ Y there, because both have property Z." Then state where it breaks. Compare two analogies side-by-side when possible. | Use an analogy because it sounds catchy. Leave the mapping implicit — readers will map the wrong features. |

**What this looks like:** Analogy is a two-column table (Source ↔ Target) with an explicit "Where the analogy breaks" row. Never a throwaway simile in prose.

---

## 6. Avoid "Dense and Lifeless" — Reverse the four failure modes

**Rule:** Technical explanations feel inert when they (1) front-load vocabulary, (2) omit motivation, (3) hide failure modes, (4) present results top-down deductively. Reverse all four.

| DO | DON'T |
|---|---|
| Start with *why anyone cares* — a problem, a paradox, a surprising observation. Show the *naive* approach failing before the sophisticated one succeeds. Use plain words first ("the thing that pushes back"), formal words second ("(restoring force)"). | Lead with a glossary. Deliver only the polished final form — readers don't learn from finished proofs; they learn from the *discovery path*. Hide where the idea breaks; failure modes are where intuition lives. |

**What this looks like:** Every chapter opens with a motivating puzzle in a highlighted card. Every concept has a "Common wrong intuition" callout showing the trap and why it fails. Jargon appears in muted text, plain-English equivalent in bold.

---

## 7. Dialogue and Socratic Questioning — Converse, don't lecture

**Rule:** A tutor asks questions that *generate* the next idea in the learner's head; a textbook tells. Questions should be answerable in 5–15 seconds — not too easy, not too hard. Good tutor questions probe assumptions, ask for predictions, request examples, surface contradictions.

| DO | DON'T |
|---|---|
| Phrase transitions as questions the reader could ask themselves ("So if doubling X doubles Y, what happens when X is negative?"). Use second-person ("you"). Address likely confusion directly ("If you're thinking 'wait, shouldn't this blow up?' — good. Here's why it doesn't."). | Write in detached third-person ("One can observe…"). Ask rhetorical questions you immediately answer — that's a lecture wearing a question mark. |

**What this looks like:** Sections are punctuated by inline questions in a distinct style (italic + indented). Each chapter ends with 2–3 retrieval prompts the reader answers before continuing. The lesson page also offers "Ask Claude to expand this" clipboard buttons so the dialogue extends into the Claude Code conversation.

---

## Anti-Patterns to Refuse

The skill should refuse to produce any lesson exhibiting these. If you catch yourself doing them, restart.

- **Definition-first openings.** "X is defined as…" with no scene set.
- **Vocabulary front-loading.** A glossary of 10 terms before any of them does work.
- **Top-down deductive flow.** Theorem → corollary → example. Reverse it.
- **Decorative animation.** Motion with no informational role.
- **Silent analogies.** "It's like a river" with no mapping table and no break-point.
- **Walls of prose.** Paragraphs >5 lines on a learning page. Break with visuals, lists, or interactions.
- **Single representation.** Equation-only, or prose-only, or picture-only. Always at least two channels, aligned.
- **Passive scrolling.** No prompts, no widgets, no predictions — the reader can finish without thinking.
- **Missing motivation.** Page 1 doesn't tell the reader *why this problem exists* or *what puzzle it solves*.
- **No failure modes.** Only the success path is shown; common wrong intuitions never named.
- **Jargon without ladders.** Technical terms introduced without a plain-English bridge.
- **Final-form-only.** Polished result with the messy discovery path erased — readers can't reconstruct the reasoning.
- **Uniform difficulty.** No desirable difficulty: every section is equally easy, so nothing sticks; or equally hard, so the reader bounces.

---

## ADEPT Framing (Better Explained shorthand)

When in doubt about how to structure a single concept:

1. **A**nalogy — connect to something the reader already knows.
2. **D**iagram — show it visually.
3. **E**xample — work a concrete instance.
4. **P**lain English — describe it without jargon.
5. **T**echnical definition — only now name the formal thing.

Always in this order. Never start with T.

---

## Sources

- Bret Victor — [Up and Down the Ladder of Abstraction](https://worrydream.com/LadderOfAbstraction/), [Explorable Explanations](https://worrydream.com/ExplorableExplanations/)
- Andy Matuschak — [How to write good prompts](https://andymatuschak.org/prompts/), [Quantum Country](https://quantum.country/)
- Grant Sanderson (3Blue1Brown) — [About](https://www.3blue1brown.com/about/)
- Nicky Case — [Explorable Explanations](https://blog.ncase.me/explorable-explanations/), [How I Make Explorable Explanations](https://blog.ncase.me/how-i-make-an-explorable-explanation/)
- Bjork & Bjork — [Creating Desirable Difficulties](https://bjorklab.psych.ucla.edu/wp-content/uploads/sites/13/2016/04/EBjork_RBjork_2011.pdf)
- Cognitive Load Theory (Sweller)
- Mayer's 12 Principles of Multimedia Learning
- Gentner — Structural vs surface analogy
- Better Explained — ADEPT method
- Worked-Example Effect
