#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["requests", "pyyaml", "beautifulsoup4"]
# ///
"""
doc-builder — Unified documentation fetcher for Claude Code skills.

Discovers, downloads, and generates 3-tier LLM-optimized documentation
from any docs site that provides llms.txt, a sitemap, or a Sphinx index.

Usage:
    doc-builder.py /path/to/docs-config.yaml

Output (written to ../references/ relative to config file):
    - Tier 1: Quick reference   (~15-30KB) — priority pages with key content
    - Tier 2: Section index     (~40-130KB) — organized summaries for topic lookup
    - Tier 3: Full docs         (~750KB-1.3MB) — complete searchable documentation
"""

import re
import sys
import time
import xml.etree.ElementTree as ET
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional
from urllib.parse import urljoin

import requests
import yaml
from bs4 import BeautifulSoup, NavigableString, Tag

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PAGE_SEPARATOR = "\u2550" * 80  # ═
SECTION_SEPARATOR = "\u2500" * 80  # ─

# ANSI colors (stderr only)
_GREEN = "\033[0;32m"
_YELLOW = "\033[1;33m"
_RED = "\033[0;31m"
_BLUE = "\033[0;34m"
_BOLD = "\033[1m"
_NC = "\033[0m"

# ---------------------------------------------------------------------------
# Logging (all output to stderr so subshell captures work)
# ---------------------------------------------------------------------------


def log_info(msg: str) -> None:
    print(f"{_GREEN}[INFO]{_NC} {msg}", file=sys.stderr)


def log_warn(msg: str) -> None:
    print(f"{_YELLOW}[WARN]{_NC} {msg}", file=sys.stderr)


def log_error(msg: str) -> None:
    print(f"{_RED}[ERROR]{_NC} {msg}", file=sys.stderr)


def log_section(msg: str) -> None:
    print(f"{_BLUE}[====]{_NC} {_BOLD}{msg}{_NC}", file=sys.stderr)


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass
class Page:
    url: str
    path: str = ""
    title: str = ""
    description: str = ""
    content: str = ""
    section: str = ""


# ---------------------------------------------------------------------------
# Config loading
# ---------------------------------------------------------------------------

_REQUIRED_KEYS = {"name", "base_url", "discovery", "output"}


def load_config(path: Path) -> dict[str, Any]:
    """Load and validate a YAML config file."""
    if not path.exists():
        log_error(f"Config file not found: {path}")
        sys.exit(1)

    with open(path, encoding="utf-8") as fh:
        config = yaml.safe_load(fh)

    if not isinstance(config, dict):
        log_error("Config file must be a YAML mapping at the top level")
        sys.exit(1)

    missing = _REQUIRED_KEYS - config.keys()
    if missing:
        log_error(f"Config missing required keys: {', '.join(sorted(missing))}")
        sys.exit(1)

    discovery = config["discovery"]
    if "method" not in discovery:
        log_error("discovery must have a 'method' key")
        sys.exit(1)
    if "url" not in discovery and "urls" not in discovery:
        log_error("discovery must have 'url' or 'urls'")
        sys.exit(1)

    if discovery["method"] not in ("sitemap", "llms_txt", "sphinx_index"):
        log_error(
            f"Unknown discovery method: {discovery['method']} "
            f"(expected 'sitemap', 'llms_txt', or 'sphinx_index')"
        )
        sys.exit(1)

    # Apply defaults
    config.setdefault("download", {})
    config["download"].setdefault("rate_limit", 0.0)
    config["download"].setdefault("timeout", 30)
    config["download"].setdefault("append_md", False)
    config["download"].setdefault("strip_suffix", None)

    config.setdefault("processing", {})
    config["processing"].setdefault("strip_frontmatter", True)
    config["processing"].setdefault("clean_blank_lines", True)

    config.setdefault("sections", {})
    config["sections"].setdefault("derive_from", None)
    config["sections"].setdefault("descriptions", {})

    output = config["output"]
    output.setdefault("quick_reference", {})
    output["quick_reference"].setdefault("file", "quick-reference.md")
    output["quick_reference"].setdefault("max_chars_per_page", 2500)
    output["quick_reference"].setdefault("priority_paths", [])

    output.setdefault("section_index", {})
    output["section_index"].setdefault("file", "section-index.md")

    output.setdefault("full_docs", {})
    output["full_docs"].setdefault("file", "full-docs.txt")

    return config


# ---------------------------------------------------------------------------
# Discovery
# ---------------------------------------------------------------------------


def discover_llms_txt(url: str, locale: Optional[str] = None) -> list[Page]:
    """Fetch llms.txt and parse '- [Title](URL): Description' lines."""
    log_section("Discovering pages from llms.txt")
    log_info(f"Fetching {url}")

    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
    except requests.RequestException as exc:
        log_error(f"Failed to fetch llms.txt: {exc}")
        sys.exit(1)

    pattern = re.compile(r"^-\s+(?:\[([^\]]*)\])?\(([^)]+)\)(?::\s*(.*))?$")
    pages: list[Page] = []

    for line in resp.text.splitlines():
        m = pattern.match(line.strip())
        if not m:
            continue
        title, page_url, description = (m.group(1) or ""), m.group(2), (m.group(3) or "").strip()

        if locale and locale not in page_url:
            continue

        pages.append(Page(url=page_url, title=title, description=description))

    log_info(f"Discovered {len(pages)} pages")
    return pages


def discover_sitemap(url: str, locale: Optional[str] = None, _depth: int = 0) -> list[Page]:
    """Fetch an XML sitemap and extract <loc> URLs.

    Handles both flat sitemaps (root <urlset>) and sitemap-index files
    (root <sitemapindex>, pointing at one or more nested sitemaps).
    For an index, recurses into each child sitemap and aggregates pages.
    Recursion is bounded by _depth ≤ 3 to guard against malformed indexes
    that point at themselves.
    """
    if _depth == 0:
        log_section("Discovering pages from sitemap")
    log_info(f"Fetching {url}")

    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
    except requests.RequestException as exc:
        log_error(f"Failed to fetch sitemap: {exc}")
        sys.exit(1)

    root = ET.fromstring(resp.content)
    ns = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}

    # Sitemap-index: contains <sitemap><loc>...</loc></sitemap> entries
    # pointing at nested sitemaps. Recurse to collect all pages.
    nested = root.findall(".//ns:sitemap/ns:loc", ns)
    if nested and _depth < 3:
        pages: list[Page] = []
        for loc in nested:
            if not loc.text:
                continue
            pages.extend(discover_sitemap(loc.text.strip(), locale, _depth + 1))
        if _depth == 0:
            pages.sort(key=lambda p: p.url)
            log_info(f"Discovered {len(pages)} pages")
        return pages

    pages: list[Page] = []
    for url_elem in root.findall(".//ns:url", ns):
        loc = url_elem.find("ns:loc", ns)
        if loc is None or not loc.text:
            continue
        page_url = loc.text.strip()

        if locale and locale not in page_url:
            continue

        pages.append(Page(url=page_url))

    pages.sort(key=lambda p: p.url)
    if _depth == 0:
        log_info(f"Discovered {len(pages)} pages")
    return pages


# ---------------------------------------------------------------------------
# Sphinx index discovery + HTML extraction
# ---------------------------------------------------------------------------


_SPHINX_NOISE_KEYWORDS = (
    "sidebar",
    "breadcrumb",
    "prev-next",
    "edit-this-page",
    "headerlink",
    "navbar",
    "toctree-wrapper",
    "search",
    "footer",
)


def _is_relative_html(href: str) -> bool:
    if not href:
        return False
    if href.startswith("#") or href.startswith("?"):
        return False
    if "://" in href or href.startswith("//") or href.startswith("mailto:"):
        return False
    if href.startswith("/"):
        return False
    base = href.split("#", 1)[0].split("?", 1)[0]
    return base.endswith(".html")


def discover_sphinx_index(urls: Any) -> list[Page]:
    """Walk one or more Sphinx index pages and collect every sibling .html link.

    Accepts a single URL string or a list. Each seed is fetched, every
    relative ``.html`` link within is resolved against the seed and added to
    the result set (deduplicated). The seed itself is also included so the
    index page's prose isn't lost.
    """
    if isinstance(urls, str):
        urls = [urls]
    elif not isinstance(urls, list):
        log_error(f"sphinx_index expects 'url' (str) or 'urls' (list), got {type(urls).__name__}")
        sys.exit(1)

    log_section("Discovering pages from Sphinx index")

    discovered: dict[str, Page] = {}

    for index_url in urls:
        log_info(f"Fetching {index_url}")
        try:
            resp = requests.get(index_url, timeout=30)
            resp.raise_for_status()
        except requests.RequestException as exc:
            log_error(f"Failed to fetch Sphinx index: {exc}")
            sys.exit(1)

        soup = BeautifulSoup(resp.text, "html.parser")
        index_title = soup.find("title")
        title_text = index_title.get_text(strip=True) if index_title else ""
        discovered.setdefault(index_url, Page(url=index_url, title=title_text))

        for anchor in soup.find_all("a", href=True):
            href = anchor["href"].strip()
            if not _is_relative_html(href):
                continue
            absolute = urljoin(index_url, href.split("#", 1)[0])
            if absolute in discovered:
                continue
            link_text = anchor.get_text(strip=True)
            discovered[absolute] = Page(url=absolute, title=link_text)

    pages = sorted(discovered.values(), key=lambda p: p.url)
    log_info(f"Discovered {len(pages)} pages")
    return pages


def _table_to_markdown(table: Tag) -> str:
    rows: list[list[str]] = []
    for tr in table.find_all("tr"):
        cells = [
            td.get_text(strip=True).replace("|", "\\|")
            for td in tr.find_all(["th", "td"])
        ]
        if cells:
            rows.append(cells)
    if not rows:
        return ""
    width = max(len(r) for r in rows)
    rows = [r + [""] * (width - len(r)) for r in rows]
    lines = ["| " + " | ".join(rows[0]) + " |"]
    lines.append("|" + "|".join("---" for _ in range(width)) + "|")
    for r in rows[1:]:
        lines.append("| " + " | ".join(r) + " |")
    return "\n\n" + "\n".join(lines) + "\n\n"


def _node_classes(node: Tag) -> str:
    if not isinstance(node, Tag) or node.attrs is None:
        return ""
    cls = node.attrs.get("class")
    if not cls:
        return ""
    if isinstance(cls, str):
        return cls.lower()
    return " ".join(cls).lower()


def _strip_sphinx_noise(scope: Tag) -> None:
    for tag in scope.find_all(["nav", "header", "footer", "script", "style", "form"]):
        tag.decompose()
    for tag in list(scope.find_all(True)):
        # decompose() in a prior iteration detaches descendants; skip them.
        if not isinstance(tag, Tag) or tag.parent is None or tag.attrs is None:
            continue
        cls = _node_classes(tag)
        role = (tag.attrs.get("role") or "").lower() if isinstance(tag.attrs.get("role"), str) else ""
        if role == "navigation":
            tag.decompose()
            continue
        if any(kw in cls for kw in _SPHINX_NOISE_KEYWORDS):
            tag.decompose()


def _html_to_markdown(root: Tag) -> str:
    def walk(node: Any) -> str:
        if isinstance(node, NavigableString):
            return re.sub(r"[ \t]+", " ", str(node))
        if not isinstance(node, Tag):
            return ""
        name = (node.name or "").lower()
        if name in ("script", "style"):
            return ""

        if name in ("h1", "h2", "h3", "h4", "h5", "h6"):
            level = int(name[1])
            text = "".join(walk(c) for c in node.children).strip()
            return f"\n\n{'#' * level} {text}\n\n"
        if name == "p":
            text = "".join(walk(c) for c in node.children).strip()
            return f"\n\n{text}\n\n" if text else ""
        if name == "pre":
            code = node.get_text()
            return f"\n\n```\n{code.rstrip()}\n```\n\n"
        if name == "code":
            text = node.get_text(strip=True)
            return f"`{text}`"
        if name == "li":
            text = "".join(walk(c) for c in node.children).strip()
            return f"- {text}\n"
        if name in ("ul", "ol"):
            text = "".join(walk(c) for c in node.children).rstrip()
            return f"\n{text}\n"
        if name in ("strong", "b"):
            text = "".join(walk(c) for c in node.children).strip()
            return f"**{text}**"
        if name in ("em", "i"):
            text = "".join(walk(c) for c in node.children).strip()
            return f"*{text}*"
        if name == "a":
            href = node.get("href", "")
            text = "".join(walk(c) for c in node.children).strip()
            if href and not href.startswith("#") and text:
                return f"[{text}]({href})"
            return text
        if name == "br":
            return "\n"
        if name == "table":
            return _table_to_markdown(node)
        if name == "hr":
            return "\n\n---\n\n"
        # Generic container — descend
        return "".join(walk(c) for c in node.children)

    text = walk(root)
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _clean_heading_text(text: str) -> str:
    # Sphinx renders headerlink anchors as `¶` or `#` next to every heading;
    # strip whichever character is left behind after the anchor is removed.
    return text.rstrip().rstrip("¶#").rstrip()


def extract_sphinx_content(html: str) -> tuple[str, str]:
    """Return (title, markdown_body) extracted from a Sphinx HTML page."""
    soup = BeautifulSoup(html, "html.parser")

    # Drop headerlink anchors site-wide so they don't pollute titles or bodies.
    for anchor in soup.find_all("a", class_="headerlink"):
        anchor.decompose()

    title = ""
    h1 = soup.find("h1")
    if h1:
        title = _clean_heading_text(h1.get_text(strip=True))
    if not title and soup.title:
        title = _clean_heading_text(soup.title.get_text(strip=True))

    main = (
        soup.find("article", attrs={"role": "main"})
        or soup.find("div", attrs={"role": "main"})
        or soup.find("article")
        or soup.find("main")
        or soup.find("div", class_="bd-article")
        or soup.find("div", class_="document")
        or soup.body
    )
    if not main:
        return title, ""

    _strip_sphinx_noise(main)
    body = _html_to_markdown(main)
    return title, body


# ---------------------------------------------------------------------------
# Content processing
# ---------------------------------------------------------------------------


def strip_frontmatter(content: str) -> str:
    """Remove YAML frontmatter between --- markers at the start of content."""
    if not content.startswith("---"):
        return content
    end = content.find("---", 3)
    if end == -1:
        return content
    return content[end + 3:].lstrip("\n")


def clean_blank_lines(content: str) -> str:
    """Collapse 3+ consecutive blank lines to 2."""
    return re.sub(r"\n{3,}", "\n\n", content)


def extract_title(content: str) -> str:
    """Extract the first # heading, or fall back to first non-empty line."""
    text = strip_frontmatter(content)
    m = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    if m:
        return m.group(1).strip()
    for line in text.split("\n"):
        line = line.strip()
        if line:
            return line[:80]
    return "Untitled"


def extract_description(content: str) -> str:
    """Extract the first paragraph after the first heading, max 200 chars."""
    text = strip_frontmatter(content)
    lines = text.split("\n")
    description_parts: list[str] = []
    found_heading = False

    for line in lines:
        if line.strip().startswith("#"):
            if found_heading and description_parts:
                break
            found_heading = True
            continue

        if found_heading and line.strip():
            description_parts.append(line.strip())
            if len(" ".join(description_parts)) > 200:
                break
        elif found_heading and not line.strip() and description_parts:
            break

    desc = " ".join(description_parts)
    if len(desc) > 200:
        desc = desc[:197] + "..."
    return desc


def get_section(url: str, base_url: str) -> str:
    """First path segment after base_url."""
    path = url.replace(base_url, "").strip("/")
    parts = path.split("/")
    return parts[0] if parts and parts[0] else "home"


def get_path(url: str, base_url: str) -> str:
    """Clean path relative to base_url."""
    path = url.replace(base_url, "")
    if not path:
        return "/"
    if not path.startswith("/"):
        path = "/" + path
    return path


def _clean_page_content(content: str, config: dict[str, Any]) -> str:
    """Apply configured processing to page content."""
    result = content
    if config["processing"]["strip_frontmatter"]:
        result = strip_frontmatter(result)
    if config["processing"]["clean_blank_lines"]:
        result = clean_blank_lines(result)
    return result.strip()


# ---------------------------------------------------------------------------
# Downloading
# ---------------------------------------------------------------------------


def download_page(url: str, timeout: int = 30) -> Optional[str]:
    """Fetch a single page and return its content, or None on failure."""
    try:
        resp = requests.get(url, timeout=timeout)
        if resp.status_code == 200:
            # requests guesses ISO-8859-1 when Content-Type has no charset,
            # which mangles UTF-8 sites like docs.nvidia.com. Prefer the
            # apparent (sniffed) encoding when no explicit charset is set.
            ct = resp.headers.get("content-type", "")
            if "charset" not in ct.lower():
                resp.encoding = resp.apparent_encoding or "utf-8"
            return resp.text
        return None
    except requests.RequestException:
        return None


def download_all(pages: list[Page], config: dict[str, Any]) -> tuple[list[Page], int]:
    """Download all pages with rate limiting. Returns (successful_pages, failure_count)."""
    base_url = config["base_url"]
    rate_limit = config["download"]["rate_limit"]
    timeout = config["download"]["timeout"]
    append_md = config["download"]["append_md"]
    strip_suffix = config["download"].get("strip_suffix")
    use_sections = config["sections"]["derive_from"] == "url_path"
    is_sphinx = config["discovery"]["method"] == "sphinx_index"

    log_section(f"Downloading {len(pages)} pages")

    successful: list[Page] = []
    failures = 0

    for i, page in enumerate(pages):
        url = page.url
        if url.endswith("/"):
            url = url.rstrip("/")

        download_url = url
        if append_md and not download_url.endswith(".md"):
            download_url = f"{url}.md"

        path_display = get_path(url, base_url)
        if strip_suffix and path_display.endswith(strip_suffix):
            path_display = path_display[: -len(strip_suffix)]
        print(
            f"  [{i + 1:3d}/{len(pages)}] {path_display}",
            end="",
            file=sys.stderr,
            flush=True,
        )

        content = download_page(download_url, timeout)

        if content is None and append_md:
            # Retry without .md suffix
            content = download_page(url, timeout)

        if content:
            if is_sphinx:
                extracted_title, body = extract_sphinx_content(content)
                page.content = body
                if extracted_title:
                    page.title = extracted_title
            else:
                page.content = content

            page.path = get_path(url, base_url)
            if strip_suffix and page.path.endswith(strip_suffix):
                page.path = page.path[: -len(strip_suffix)]

            if not page.title:
                page.title = extract_title(page.content)
            if not page.description:
                page.description = extract_description(page.content)
            if use_sections and not page.section:
                page.section = get_section(url, base_url)

            if is_sphinx and not page.content.strip():
                failures += 1
                print(f" {_YELLOW}empty body, skipped{_NC}", file=sys.stderr)
                continue

            successful.append(page)
            title_short = page.title[:40]
            print(f" {_GREEN}ok{_NC} {title_short}", file=sys.stderr)
        else:
            failures += 1
            print(f" {_RED}FAIL{_NC}", file=sys.stderr)

        if rate_limit > 0:
            time.sleep(rate_limit)

    print(file=sys.stderr)
    log_info(f"Fetched {len(successful)} pages ({failures} failed)")

    if len(successful) < 10:
        log_error("Too few pages fetched (<10). Aborting.")
        sys.exit(1)

    if len(pages) > 0:
        failure_pct = failures / len(pages) * 100
        if failure_pct > 20:
            log_warn(f"High failure rate: {failure_pct:.0f}% ({failures}/{len(pages)})")

    return successful, failures


# ---------------------------------------------------------------------------
# Tier 1: Quick Reference
# ---------------------------------------------------------------------------


def generate_quick_reference(pages: list[Page], config: dict[str, Any]) -> str:
    """Generate Tier 1 quick-reference with priority pages."""
    name = config["name"]
    base_url = config["base_url"]
    qr_config = config["output"]["quick_reference"]
    max_chars = qr_config["max_chars_per_page"]
    priority_paths = qr_config["priority_paths"]
    use_sections = config["sections"]["derive_from"] == "url_path"
    section_descs = config["sections"].get("descriptions", {})
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    out: list[str] = []
    out.append(f"# {name} Quick Reference")
    out.append("")
    out.append(f"Source: {base_url}")
    out.append(f"Generated: {now}")
    out.append("")

    # Build a lookup by path
    by_path: dict[str, Page] = {p.path: p for p in pages}

    # Navigation table (if sections exist)
    if use_sections:
        sections: dict[str, list[Page]] = defaultdict(list)
        for p in pages:
            sections[p.section].append(p)

        out.append("## Quick Navigation")
        out.append("")
        out.append("| Section | Pages | Description |")
        out.append("|---------|-------|-------------|")
        for sec in sorted(sections.keys()):
            desc = section_descs.get(sec, "")
            out.append(f"| {sec} | {len(sections[sec])} | {desc} |")
        out.append("")

    # Determine which pages to include
    if priority_paths:
        selected: list[Page] = []
        for ppath in priority_paths:
            if ppath in by_path:
                selected.append(by_path[ppath])
            else:
                # Try partial match (path may not have trailing slash, etc.)
                for p in pages:
                    if p.path.rstrip("/") == ppath.rstrip("/"):
                        selected.append(p)
                        break
    else:
        # No priority paths: include first 10 pages sorted by path
        selected = sorted(pages, key=lambda p: p.path)[:10]

    # Render selected pages
    for page in selected:
        cleaned = _clean_page_content(page.content, config)

        # Remove duplicate title
        title_line = f"# {page.title}"
        if cleaned.startswith(title_line):
            cleaned = cleaned[len(title_line):].strip()

        out.append(f"### {page.title}")
        out.append(f"*Source: {page.path}*")
        out.append("")

        if len(cleaned) > max_chars:
            cut = cleaned.rfind("\n\n", 0, max_chars)
            if cut > max_chars * 0.6:
                cleaned = cleaned[:cut] + "\n\n*[See full documentation for more...]*"
            else:
                cleaned = cleaned[:max_chars] + "\n\n*[See full documentation for more...]*"

        out.append(cleaned)
        out.append("")
        out.append(SECTION_SEPARATOR)
        out.append("")

    return "\n".join(out)


# ---------------------------------------------------------------------------
# Tier 2: Section Index
# ---------------------------------------------------------------------------


def generate_section_index(pages: list[Page], config: dict[str, Any]) -> str:
    """Generate Tier 2 section index with organized summaries."""
    name = config["name"]
    use_sections = config["sections"]["derive_from"] == "url_path"
    section_descs = config["sections"].get("descriptions", {})
    full_docs_file = config["output"]["full_docs"]["file"]

    out: list[str] = []
    out.append(f"# {name} Documentation Index")
    out.append("")
    out.append("Organized reference for finding topics.")
    out.append(f"Use grep on `{full_docs_file}` for full content.")
    out.append("")

    if use_sections:
        # Group by section
        sections: dict[str, list[Page]] = defaultdict(list)
        for p in pages:
            sections[p.section].append(p)

        # Overview table
        out.append("## Sections Overview")
        out.append("")
        out.append("| Section | Pages | Description |")
        out.append("|---------|-------|-------------|")
        for sec in sorted(sections.keys()):
            desc = section_descs.get(sec, "Documentation section")
            out.append(f"| [{sec.upper()}](#{sec}) | {len(sections[sec])} | {desc} |")
        out.append("")

        # Per-section listings
        for sec in sorted(sections.keys()):
            sec_pages = sorted(sections[sec], key=lambda p: p.path)
            desc = section_descs.get(sec, "")

            out.append(PAGE_SEPARATOR)
            out.append(f"## {sec.upper()}")
            if desc:
                out.append(f"*{desc}*")
            out.append("")
            out.append(f"**{len(sec_pages)} pages in this section:**")
            out.append("")

            for page in sec_pages:
                out.append(f"### {page.title}")
                out.append(f"**Path:** `{page.path}`")
                if page.description:
                    out.append(f"**Summary:** {page.description}")
                out.append("")

            out.append("")
    else:
        # Flat alphabetical listing
        out.append("## All Pages")
        out.append("")
        sorted_pages = sorted(pages, key=lambda p: p.title.lower())
        for page in sorted_pages:
            out.append(f"### {page.title}")
            out.append(f"**Path:** `{page.path}`")
            if page.description:
                out.append(f"**Summary:** {page.description}")
            out.append("")

    # Grep patterns guide
    out.append(PAGE_SEPARATOR)
    out.append("## Search Patterns")
    out.append("")
    out.append(f"Use these grep patterns to find content in `{full_docs_file}`:")
    out.append("")
    out.append("```bash")
    out.append("# Find a specific page")
    out.append(f'grep -A 100 "^PAGE: /path" {full_docs_file}')
    out.append("")
    if use_sections:
        out.append("# Find all pages in a section")
        out.append(f'grep -B 1 "^SECTION: SECTIONNAME" {full_docs_file} | grep "^PAGE:"')
        out.append("")
    out.append("# Extract a complete page (between separators)")
    out.append(f'sed -n "/^PAGE: \\/your-page$/,/^\\xe2\\x95\\x90\\{{80\\}}$/p" {full_docs_file}')
    out.append("")
    out.append("# Search for a keyword across all docs")
    out.append(f'grep -n "keyword" {full_docs_file}')
    out.append("```")
    out.append("")

    return "\n".join(out)


# ---------------------------------------------------------------------------
# Tier 3: Full Documentation
# ---------------------------------------------------------------------------


def generate_full_docs(pages: list[Page], config: dict[str, Any]) -> str:
    """Generate Tier 3 complete documentation with grep-friendly markers."""
    name = config["name"]
    base_url = config["base_url"]
    use_sections = config["sections"]["derive_from"] == "url_path"
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    out: list[str] = []

    # File header
    out.append(PAGE_SEPARATOR)
    out.append(f"{name.upper()} - COMPLETE DOCUMENTATION")
    out.append(f"Source: {base_url}")
    out.append(f"Generated: {now}")
    out.append(f"Total Pages: {len(pages)}")
    out.append("Format: LLM-optimized with grep-friendly page markers")
    out.append(PAGE_SEPARATOR)
    out.append("")
    out.append("SEARCH PATTERNS:")
    out.append("  Find page:    grep -A 100 '^PAGE: /path' <file>")
    if use_sections:
        out.append("  Find section: grep '^SECTION: NAME' <file>")
    out.append("  Find keyword: grep -n 'keyword' <file>")
    out.append("")
    out.append(PAGE_SEPARATOR)
    out.append("")

    if use_sections:
        # Group by section
        sections: dict[str, list[Page]] = defaultdict(list)
        for p in pages:
            sections[p.section].append(p)

        for sec in sorted(sections.keys()):
            sec_pages = sorted(sections[sec], key=lambda p: p.path)

            out.append(SECTION_SEPARATOR)
            out.append(f"SECTION GROUP: {sec.upper()}")
            out.append(f"Pages: {len(sec_pages)}")
            out.append(SECTION_SEPARATOR)
            out.append("")

            for page in sec_pages:
                cleaned = _clean_page_content(page.content, config)

                out.append(PAGE_SEPARATOR)
                out.append(f"PAGE: {page.path}")
                out.append(f"SECTION: {sec.upper()}")
                out.append(f"TITLE: {page.title}")
                out.append(PAGE_SEPARATOR)
                out.append("")
                out.append(cleaned)
                out.append("")

            out.append("")
    else:
        # Flat: sorted by path
        sorted_pages = sorted(pages, key=lambda p: p.path)
        for page in sorted_pages:
            cleaned = _clean_page_content(page.content, config)

            out.append(PAGE_SEPARATOR)
            out.append(f"PAGE: {page.path}")
            out.append(f"TITLE: {page.title}")
            out.append(PAGE_SEPARATOR)
            out.append("")
            out.append(cleaned)
            out.append("")

    # Footer
    out.append(PAGE_SEPARATOR)
    out.append("END OF DOCUMENTATION")
    out.append(PAGE_SEPARATOR)

    return "\n".join(out)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    if len(sys.argv) < 2:
        log_error("Usage: doc-builder.py <config.yaml>")
        sys.exit(1)

    config_path = Path(sys.argv[1]).resolve()
    config = load_config(config_path)

    name = config["name"]
    log_section(f"doc-builder: {name}")

    # Resolve output directory relative to config file location
    refs_dir = config_path.parent / "references"
    refs_dir = refs_dir.resolve()
    refs_dir.mkdir(parents=True, exist_ok=True)
    log_info(f"Output directory: {refs_dir}")

    # ---- Discovery ----
    discovery = config["discovery"]
    locale = discovery.get("locale")
    method = discovery["method"]

    if method == "llms_txt":
        pages = discover_llms_txt(discovery["url"], locale)
    elif method == "sphinx_index":
        seeds = discovery.get("urls") or discovery["url"]
        pages = discover_sphinx_index(seeds)
    else:
        pages = discover_sitemap(discovery["url"], locale)

    if not pages:
        log_error("No pages discovered. Aborting.")
        sys.exit(1)

    # ---- Extra pages (appended after discovery) ----
    extra = discovery.get("extra_pages", [])
    if extra:
        for ep in extra:
            pages.append(Page(url=ep["url"], title=ep.get("title", ""), description=ep.get("description", "")))
        log_info(f"Added {len(extra)} extra pages (total: {len(pages)})")

    # ---- Download ----
    pages, failures = download_all(pages, config)

    # Populate section from URL path if configured
    if config["sections"]["derive_from"] == "url_path":
        base_url = config["base_url"]
        for page in pages:
            if not page.section:
                page.section = get_section(page.url, base_url)

    # ---- Generate Tier 1: Quick Reference ----
    qr_file = refs_dir / config["output"]["quick_reference"]["file"]
    log_info(f"Generating Tier 1: {qr_file.name}")
    quick_ref = generate_quick_reference(pages, config)
    qr_file.write_text(quick_ref, encoding="utf-8")
    qr_size = len(quick_ref)
    log_info(f"  -> {qr_size:,} chars ({qr_size // 1024}KB)")

    # ---- Generate Tier 2: Section Index ----
    si_file = refs_dir / config["output"]["section_index"]["file"]
    log_info(f"Generating Tier 2: {si_file.name}")
    section_idx = generate_section_index(pages, config)
    si_file.write_text(section_idx, encoding="utf-8")
    si_size = len(section_idx)
    log_info(f"  -> {si_size:,} chars ({si_size // 1024}KB)")

    # ---- Generate Tier 3: Full Documentation ----
    fd_file = refs_dir / config["output"]["full_docs"]["file"]
    log_info(f"Generating Tier 3: {fd_file.name}")
    full_docs = generate_full_docs(pages, config)
    fd_file.write_text(full_docs, encoding="utf-8")
    fd_size = len(full_docs)
    log_info(f"  -> {fd_size:,} chars ({fd_size // 1024}KB)")

    # ---- Summary ----
    print(file=sys.stderr)
    print("=" * 60, file=sys.stderr)
    print(f"  {name} — build complete", file=sys.stderr)
    print("=" * 60, file=sys.stderr)
    print(f"  Pages fetched:  {len(pages)}", file=sys.stderr)
    print(f"  Pages failed:   {failures}", file=sys.stderr)
    print(file=sys.stderr)
    print("  Output files:", file=sys.stderr)
    print(f"    Tier 1: {qr_file.name:30s} {qr_size // 1024:>5}KB", file=sys.stderr)
    print(f"    Tier 2: {si_file.name:30s} {si_size // 1024:>5}KB", file=sys.stderr)
    print(f"    Tier 3: {fd_file.name:30s} {fd_size // 1024:>5}KB", file=sys.stderr)
    print("=" * 60, file=sys.stderr)


if __name__ == "__main__":
    main()
