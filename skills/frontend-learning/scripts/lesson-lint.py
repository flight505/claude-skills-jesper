#!/usr/bin/env python3
"""
lesson-lint.py — static linter for frontend-learning HTML lessons.

Layer A of the two-layer QA model. Runs in seconds, deterministic, no model
calls, no screenshots. Replaces the manual Quality Bar checklist as the only
mandatory quality gate.

Usage:
    ./scripts/lesson-lint.py path/to/lesson.html
    ./scripts/lesson-lint.py path/to/lesson.html --plain   # no ANSI colors

Exit codes:
    0 — all HARD checks passed (soft warnings are not blocking)
    1 — one or more HARD checks failed
    2 — usage / file error
"""

from __future__ import annotations

import argparse
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from typing import Callable


# ---------------------------------------------------------------------------
# HTML model — collected by a single pass of HTMLParser
# ---------------------------------------------------------------------------

class LessonHTML(HTMLParser):
    """Single-pass collector. We capture only what the linter needs."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        # Counts / collections
        self.tag_stack: list[tuple[str, dict[str, str | None]]] = []
        self.style_text_chunks: list[str] = []
        self._in_style = False
        self.title_text = ""
        self._in_title = False
        # Structural presence
        self.has_div_lesson_with_article = False
        self.has_progress = False
        self.has_concept_map_fixed = False
        self.has_concept_map_mobile = False
        self.section_ids: list[str] = []
        self.toc_data_sections: list[str] = []
        self.ask_claude_prompts: list[str] = []
        self.wrong_intuition_count = 0
        self.retrieval_count = 0
        self.predict_count = 0
        self.quiz_count = 0
        self.adept_count = 0
        self.section_tag_count = 0
        self.meta_description = ""
        # KaTeX
        self.katex_css_loaded = False
        self.katex_js_loaded = False
        self.katex_autorender_loaded = False
        # SVG-inside-widget tracking
        self.widget_depth = 0
        self.svg_inside_widget_issues: list[str] = []
        self.current_svg_attrs: dict[str, str | None] | None = None
        # Body raw text for placeholder check (post-parse)
        self.body_chunks: list[str] = []
        self._in_body = False
        # CSS-text patterns
        self._inline_css = ""  # populated after parse

    # ------- Helpers -------

    @staticmethod
    def _classes(attrs: dict[str, str | None]) -> set[str]:
        c = attrs.get("class") or ""
        return set(c.split())

    @staticmethod
    def _attr(attrs: list[tuple[str, str | None]]) -> dict[str, str | None]:
        return dict(attrs)

    # ------- Parser callbacks -------

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = self._attr(attrs)
        self.tag_stack.append((tag, a))
        cls = self._classes(a)

        if tag == "title":
            self._in_title = True
        if tag == "body":
            self._in_body = True
        if tag == "style":
            self._in_style = True
        if tag == "meta" and (a.get("name") or "").lower() == "description":
            self.meta_description = (a.get("content") or "").strip()

        # KaTeX CDN loads
        href = (a.get("href") or "").lower()
        src = (a.get("src") or "").lower()
        if tag == "link" and "katex" in href and "katex.min.css" in href:
            self.katex_css_loaded = True
        if tag == "script":
            if "katex.min.js" in src:
                self.katex_js_loaded = True
            if "auto-render.min.js" in src:
                self.katex_autorender_loaded = True

        # Article inside .lesson
        if tag == "article":
            # Walk stack outward looking for a div.class=lesson ancestor
            for ancestor_tag, ancestor_attrs in reversed(self.tag_stack[:-1]):
                if ancestor_tag == "div" and "lesson" in self._classes(ancestor_attrs):
                    self.has_div_lesson_with_article = True
                    break

        # Progress bar
        if tag == "div" and a.get("id") == "progress":
            self.has_progress = True

        # Concept maps (responsive TOC)
        if tag == "nav" and "concept-map-fixed" in cls:
            self.has_concept_map_fixed = True
        if tag == "details" and "concept-map-mobile" in cls:
            self.has_concept_map_mobile = True

        # Section IDs (inside <article>)
        sid = a.get("id")
        if tag == "section" and sid:
            self.section_ids.append(sid)
        if tag == "section":
            self.section_tag_count += 1

        # TOC entries
        ds = a.get("data-section")
        if tag == "li" and ds:
            self.toc_data_sections.append(ds)

        # Ask-Claude buttons
        if tag == "button" and "ask-claude" in cls:
            self.ask_claude_prompts.append((a.get("data-prompt") or "").strip())

        # Pedagogical callouts
        if tag in ("aside", "div", "section") and "wrong-intuition" in cls:
            self.wrong_intuition_count += 1
        if tag in ("section", "div") and "retrieval" in cls:
            self.retrieval_count += 1
        if tag == "div" and "predict" in cls:
            self.predict_count += 1
        if tag == "div" and "quiz" in cls:
            self.quiz_count += 1
        if tag == "article" and "adept" in cls:
            self.adept_count += 1

        # Widget / SVG tracking
        if tag == "div" and "widget" in cls:
            self.widget_depth += 1
        if tag == "svg":
            if self.widget_depth > 0:
                # SVGs inside widgets MUST use viewBox and MUST NOT have width/height
                problems = []
                if not a.get("viewbox") and not a.get("viewBox"):
                    # html.parser lowercases attr names; viewbox is correct lookup
                    if not a.get("viewbox"):
                        problems.append("missing viewBox attribute")
                if a.get("width"):
                    problems.append(f"has width={a['width']!r} (use viewBox only)")
                if a.get("height"):
                    problems.append(f"has height={a['height']!r} (use viewBox only)")
                if problems:
                    self.svg_inside_widget_issues.append(
                        f"SVG #{len(self.svg_inside_widget_issues) + 1} in widget: " + ", ".join(problems)
                    )

    def handle_endtag(self, tag: str) -> None:
        # Pop matching tag (cheap, tolerant)
        for i in range(len(self.tag_stack) - 1, -1, -1):
            if self.tag_stack[i][0] == tag:
                cls = self._classes(self.tag_stack[i][1])
                if tag == "div" and "widget" in cls:
                    self.widget_depth = max(0, self.widget_depth - 1)
                del self.tag_stack[i:]
                break
        if tag == "title":
            self._in_title = False
        if tag == "body":
            self._in_body = False
        if tag == "style":
            self._in_style = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title_text += data
        if self._in_style:
            self.style_text_chunks.append(data)
        if self._in_body:
            self.body_chunks.append(data)

    # ------- Post-parse derived -------

    def finish(self) -> None:
        self._inline_css = "\n".join(self.style_text_chunks)


# ---------------------------------------------------------------------------
# Check engine
# ---------------------------------------------------------------------------

class CheckResult:
    __slots__ = ("severity", "name", "passed", "message")

    def __init__(self, severity: str, name: str, passed: bool, message: str = "") -> None:
        assert severity in ("HARD", "SOFT")
        self.severity = severity
        self.name = name
        self.passed = passed
        self.message = message


CHECKS: list[Callable[[LessonHTML, str], CheckResult]] = []


def check(severity: str, name: str):
    def decorator(fn: Callable[[LessonHTML, str], CheckResult | tuple[bool, str]]):
        def wrapped(doc: LessonHTML, raw: str) -> CheckResult:
            result = fn(doc, raw)
            if isinstance(result, CheckResult):
                return result
            passed, message = result
            return CheckResult(severity, name, passed, message)
        CHECKS.append(wrapped)
        return wrapped
    return decorator


# ---- HARD checks ----

@check("HARD", "div.lesson wraps <article>")
def _c_lesson_wraps_article(doc, raw):
    if doc.has_div_lesson_with_article:
        return True, ""
    return False, "no <article> found inside a <div class=\"lesson\">; the CSS Grid layout requires this wrapper"


@check("HARD", "reading-progress bar (<div id=\"progress\">)")
def _c_progress(doc, raw):
    if doc.has_progress:
        return True, ""
    return False, "missing <div id=\"progress\"></div> at the top of <body>"


@check("HARD", "responsive TOC: both concept-map-fixed and concept-map-mobile")
def _c_toc(doc, raw):
    missing = []
    if not doc.has_concept_map_fixed:
        missing.append("<nav class=\"concept-map-fixed\">")
    if not doc.has_concept_map_mobile:
        missing.append("<details class=\"concept-map-mobile\">")
    if not missing:
        return True, ""
    return False, "missing " + " and ".join(missing) + " (both required for responsive TOC)"


@check("HARD", "inlined <style> block ≥ 5000 chars (lesson-base.css present)")
def _c_inline_css_size(doc, raw):
    size = len(doc._inline_css)
    if size >= 5000:
        return True, ""
    return False, f"inlined <style> block is {size} chars; lesson-base.css must be inlined (~13000 chars). Did you skip inlining?"


@check("HARD", "KaTeX loaded (css + js + auto-render)")
def _c_katex(doc, raw):
    missing = []
    if not doc.katex_css_loaded:
        missing.append("katex.min.css")
    if not doc.katex_js_loaded:
        missing.append("katex.min.js")
    if not doc.katex_autorender_loaded:
        missing.append("auto-render.min.js")
    if not missing:
        return True, ""
    return False, "missing KaTeX CDN loads: " + ", ".join(missing)


@check("HARD", "≥ 4 .ask-claude buttons with non-empty data-prompt")
def _c_ask_claude_count(doc, raw):
    total = len(doc.ask_claude_prompts)
    nonempty = [p for p in doc.ask_claude_prompts if p]
    if len(nonempty) >= 4:
        return True, ""
    return False, f"found {total} .ask-claude buttons ({len(nonempty)} with non-empty data-prompt); need ≥ 4 with prompts"


@check("HARD", "all .ask-claude data-prompt strings unique")
def _c_ask_claude_unique(doc, raw):
    prompts = [p for p in doc.ask_claude_prompts if p]
    seen = set()
    dupes = set()
    for p in prompts:
        if p in seen:
            dupes.add(p[:60] + ("..." if len(p) > 60 else ""))
        seen.add(p)
    if not dupes:
        return True, ""
    return False, f"{len(dupes)} duplicate prompt(s): " + " | ".join(sorted(dupes))


@check("HARD", "TOC ↔ sections: every data-section matches a section[id]")
def _c_toc_to_sections(doc, raw):
    section_set = set(doc.section_ids)
    orphans = [d for d in doc.toc_data_sections if d not in section_set]
    if not orphans:
        return True, ""
    return False, f"TOC has data-section value(s) with no matching section[id]: {sorted(set(orphans))}"


@check("HARD", "TOC ↔ sections: every section[id] appears in TOC")
def _c_sections_to_toc(doc, raw):
    toc_set = set(doc.toc_data_sections)
    missing = [s for s in doc.section_ids if s not in toc_set]
    if not missing:
        return True, ""
    return False, f"section[id] not referenced by any TOC entry: {sorted(set(missing))}"


@check("HARD", "SVGs inside widgets use viewBox (no fixed width/height)")
def _c_svg_responsive(doc, raw):
    if not doc.svg_inside_widget_issues:
        return True, ""
    issues = "; ".join(doc.svg_inside_widget_issues[:5])
    more = "" if len(doc.svg_inside_widget_issues) <= 5 else f"  (and {len(doc.svg_inside_widget_issues) - 5} more)"
    return False, issues + more


@check("HARD", "no unfilled {{template}} placeholders left in body")
def _c_placeholders(doc, raw):
    body = "".join(doc.body_chunks)
    # Look for double-curly placeholders typical of template/Mustache style
    found = sorted(set(re.findall(r"\{\{\s*[a-zA-Z_][\w_]*\s*\}\}", body)))
    if not found:
        return True, ""
    return False, "unfilled placeholders: " + ", ".join(found[:8])


@check("HARD", "≥ 1 .wrong-intuition callout")
def _c_wrong(doc, raw):
    if doc.wrong_intuition_count >= 1:
        return True, ""
    return False, "no .wrong-intuition callout found (every lesson should name a common misconception)"


@check("HARD", "≥ 1 .retrieval block")
def _c_retrieval(doc, raw):
    if doc.retrieval_count >= 1:
        return True, ""
    return False, "no .retrieval block found (every lesson should end with retrieval prompts)"


@check("HARD", "≥ 1 .predict or .quiz block")
def _c_engagement(doc, raw):
    if doc.predict_count + doc.quiz_count >= 1:
        return True, ""
    return False, "no .predict or .quiz block found (every lesson needs ≥ 1 active-engagement widget)"


@check("HARD", "prefers-reduced-motion media query present in inlined CSS")
def _c_reduced_motion(doc, raw):
    if "prefers-reduced-motion" in doc._inline_css:
        return True, ""
    return False, "inlined CSS missing @media (prefers-reduced-motion: reduce) rule"


# ---- SOFT checks ----

@check("SOFT", "color-coded variable CSS rules present (.var-q/k/v or .var-x/y/z)")
def _c_color_vars(doc, raw):
    css = doc._inline_css
    qkv = bool(re.search(r"\.var-[qkv]\b", css))
    xyz = bool(re.search(r"\.var-[xyz]\b", css))
    if qkv or xyz:
        return True, ""
    return False, "no .var-q/k/v or .var-x/y/z rules in CSS; color-coding across prose/equation/diagram may be missing"


@check("SOFT", "<title> non-empty")
def _c_title(doc, raw):
    if doc.title_text.strip():
        return True, ""
    return False, "empty or missing <title>"


@check("SOFT", "<meta name=\"description\"> non-empty")
def _c_description(doc, raw):
    if doc.meta_description:
        return True, ""
    return False, "empty or missing <meta name=\"description\">"


@check("SOFT", "≥ 3 <section> elements")
def _c_section_count(doc, raw):
    if doc.section_tag_count >= 3:
        return True, ""
    return False, f"only {doc.section_tag_count} <section> elements; lessons typically have 6–8"


# ---------------------------------------------------------------------------
# Reporter
# ---------------------------------------------------------------------------

def report(results: list[CheckResult], path: Path, use_color: bool) -> int:
    if use_color and sys.stdout.isatty():
        RED, YEL, GRN, DIM, RST = "\033[31m", "\033[33m", "\033[32m", "\033[2m", "\033[0m"
    else:
        RED = YEL = GRN = DIM = RST = ""

    hard_fail = [r for r in results if r.severity == "HARD" and not r.passed]
    soft_fail = [r for r in results if r.severity == "SOFT" and not r.passed]
    passed = [r for r in results if r.passed]

    print(f"\n{DIM}lesson-lint{RST}  {path}\n")

    for r in results:
        if r.passed:
            sym, color = "✓", GRN
            line = f"  {color}{sym}{RST} {DIM}{r.severity}{RST} {r.name}"
        else:
            sym, color = "✗", RED if r.severity == "HARD" else YEL
            line = f"  {color}{sym} {r.severity}{RST} {r.name}\n      {color}→ {r.message}{RST}"
        print(line)

    print()
    summary = (
        f"  {GRN}{len(passed)} passed{RST}"
        f"  ·  {RED}{len(hard_fail)} HARD failed{RST}"
        f"  ·  {YEL}{len(soft_fail)} soft warnings{RST}"
    )
    print(summary)

    if hard_fail:
        print(f"\n  {RED}NOT READY{RST} — fix HARD failures before opening the lesson.\n")
        return 1
    if soft_fail:
        print(f"\n  {GRN}READY{RST} — soft warnings are advisory, lesson can be opened.\n")
    else:
        print(f"\n  {GRN}READY{RST} — all checks passed.\n")
    return 0


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=(__doc__ or "").strip().splitlines()[0])
    ap.add_argument("lesson", help="path to .html lesson file")
    ap.add_argument("--plain", action="store_true", help="disable ANSI colors")
    args = ap.parse_args()

    path = Path(args.lesson)
    if not path.exists():
        print(f"lesson-lint: file not found: {path}", file=sys.stderr)
        return 2
    if not path.is_file():
        print(f"lesson-lint: not a regular file: {path}", file=sys.stderr)
        return 2

    raw = path.read_text(encoding="utf-8", errors="replace")
    doc = LessonHTML()
    try:
        doc.feed(raw)
        doc.close()
    except Exception as e:
        print(f"lesson-lint: HTML parse failed: {e}", file=sys.stderr)
        return 2
    doc.finish()

    results = [c(doc, raw) for c in CHECKS]
    return report(results, path, use_color=not args.plain)


if __name__ == "__main__":
    sys.exit(main())
