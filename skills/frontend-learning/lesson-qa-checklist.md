# Lesson Visual-QA Checklist  (Layer B — what eyes catch that the linter can't)

The `lesson-reviewer` subagent applies this checklist to ONE full-page screenshot per viewport (1920×1080, 1280×800, 768×1024, 375×667). It does NOT scroll, does NOT re-check, has a hard 10-tool-call budget.

**Layer A (`scripts/lesson-lint.py`) already covers:** required elements, TOC ↔ section bidirectional match, ≥4 unique ask-claude prompts, no fixed-width SVGs in widgets, ≥1 of each callout type, prefers-reduced-motion in CSS, no unfilled placeholders. **Don't repeat those here.**

Items below are the things only a rendered screenshot reveals — visual quirks, overflow, cramping, contrast, math-render correctness. Each item is `[VISUAL]` and scored PASS / FAIL with specifics.

---

## Layout & spacing

1. **HARD** — On 1920×1080, is the article visually anchored to the page (centered, with the sticky TOC docking on the left), or does it look marooned in a dark void with most of the viewport empty?
2. **HARD** — On 1920×1080 and 1280×800, does the sticky concept-map TOC overlap or collide with the article content or any widget?
3. **HARD** — On 375×667 (mobile), does ANY content cause horizontal *page* scroll? (Vertical scroll inside `<pre>` or `.katex-display` is OK; *page-level* horizontal scroll is a failure.)
4. On 768×1024 (tablet), is the responsive TOC present as the collapsible `<details>` dropdown at the top (and the fixed sidebar is gone)?
5. Is whitespace between sections comfortable at each viewport (not cramped, not yawning)?

## Widgets

6. **HARD** — On every viewport, does each widget fit within its card border? Any text/SVG spilling outside the rounded edge?
7. **HARD** — In any widget containing an SVG matrix, plot, or chart: are cell values / labels legible (no overlapping characters)? A 4-character value like `-0.31` must have visible padding on both sides.
8. Do range sliders take available width without overflowing on narrow viewports?
9. Are buttons / interactive controls tap-friendly on mobile (≥40px tall)?

## Typography

10. **HARD** — Is body text legible on mobile (effective size ≥14px)? If text is too tiny to read on the screenshot, fail.
11. Are headings well-proportioned to body at every viewport (not towering on mobile, not anaemic on desktop)?

## Math (KaTeX)

12. **HARD** — Has KaTeX rendered? (Any literal `$…$` or `$$…$$` LaTeX visible in body text = KaTeX failed to run — usually a delimiter typo or script load failure.)
13. **HARD** — Does any display-math equation cause horizontal *page* scroll? (Inline scroll within `.katex-display` is OK and expected.)
14. Are color-coded variables visible in the rendered math? (If the prose has orange `Q`, the equation's `Q` should also be orange.)

## Color & contrast

15. **HARD** — Is body text contrast sufficient against background? (No grey-on-grey that disappears.)
16. Are pedagogical callouts (predict, quiz, wrong-intuition, retrieval) clearly distinct by color, but harmonious with the overall theme?
17. Do "Ask Claude" buttons read as interactive (visibly a button, not stray text)?

---

## Output format the reviewer uses

```markdown
## Visual QA report — <filename>

### 1920×1080
- [PASS] 1. Article anchored
- [FAIL] 7. §5 worked example: SVG matrix cells ~28px wide, values like `-0.31` smush into adjacent cell
- ...

### 1280×800
- ...

### 768×1024
- ...

### 375×667
- ...

## Summary
- HARD failures: N — must fix before opening
  - <one-line each>
- Soft failures: M
- Overall: READY  |  NOT READY  |  TIMED OUT
```

Main session reads this and applies targeted fixes. Items NOT in this list (e.g. "≥4 ask-claude buttons", "TOC matches sections") are the linter's job — agent doesn't repeat them.
