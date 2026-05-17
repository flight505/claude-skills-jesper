#!/usr/bin/env python3
"""Regenerate .claude-plugin/marketplace.json from upstream/ + skills/.

Sources:
  1. upstream/.claude-plugin/marketplace.json  — domain bundles (emitted as plugins[])
  2. skills/<name>/SKILL.md                    — first-party skills, depth-capped:
                                                  nested SKILL.md under skills/ are
                                                  staged content and NOT exposed

Bundle-internal SKILL.md files (upstream/<bundle>/skills/...) are intentionally
NOT emitted as standalone entries in skills[] — they install with their parent
plugin. The OVERLAP.md merge path is preserved for forward-compat but is a
no-op for skills[] under this scheme.

Forge schema reference:
  - internal/schemas/types.go — Entry, MarketplaceFile
  - SourceRef accepts either a string path or {source, path, type} object
  - First-class types: skill, plugin, agent, persona, command (since L2-A)
  - Unknown Entry fields are silently ignored by forge (json.Unmarshal lenient)

This script uses only the standard library.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
UPSTREAM_DIR = ROOT / "upstream"
SKILLS_DIR = ROOT / "skills"
OUT_PATH = ROOT / ".claude-plugin" / "marketplace.json"
OVERLAP_PATH = ROOT / "OVERLAP.md"
UPSTREAM_MARKETPLACE = UPSTREAM_DIR / ".claude-plugin" / "marketplace.json"

# Roots for non-skill content. Personas live in agents/personas/; everything
# else under agents/ is an agent. Commands are walked from the top-level
# commands/ dir only — bundle-internal commands ride along with their plugin
# install and are not promoted to the top-level commands[] array.
PERSONAS_ROOT = UPSTREAM_DIR / "agents" / "personas"
AGENTS_ROOT = UPSTREAM_DIR / "agents"
COMMANDS_ROOT = UPSTREAM_DIR / "commands"

# .md filenames we never treat as installable content.
META_FILENAMES = {"README.md", "TEMPLATE.md", "CHANGELOG.md", "CLAUDE.md", "GEMINI.md", "AGENTS.md"}

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*(?:\n|$)", re.DOTALL)
TOP_KEY_RE = re.compile(r"^([a-zA-Z_][\w-]*)\s*:\s*(.*?)\s*$")
NESTED_KEY_RE = re.compile(r"^[ \t]+([a-zA-Z_][\w-]*)\s*:\s*(.*?)\s*$")


def strip_quotes(s: str) -> str:
    s = s.strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in ('"', "'"):
        return s[1:-1]
    return s


def parse_frontmatter(text: str) -> dict[str, Any]:
    """Minimal YAML frontmatter parser. Handles top-level scalars + one level
    of nesting under a key (e.g. `metadata:`). Multi-line values are joined.
    """
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    body = m.group(1)
    out: dict[str, Any] = {}
    current_parent: str | None = None
    pending_key: str | None = None
    pending_lines: list[str] = []

    def flush_pending(target: dict[str, Any]) -> None:
        nonlocal pending_key, pending_lines
        if pending_key is None:
            return
        target[pending_key] = " ".join(p.strip() for p in pending_lines).strip()
        pending_key = None
        pending_lines = []

    for raw in body.splitlines():
        target_now = out if current_parent is None else out[current_parent]
        if not raw.strip() or raw.lstrip().startswith("#"):
            flush_pending(target_now)
            continue
        nested = NESTED_KEY_RE.match(raw) if current_parent is not None else None
        top = TOP_KEY_RE.match(raw)
        if nested and current_parent is not None:
            flush_pending(out[current_parent])
            key, val = nested.group(1), nested.group(2)
            if val == "":
                pending_key = key
                pending_lines = []
            else:
                out[current_parent][key] = strip_quotes(val)
        elif top:
            target = out if current_parent is None else out[current_parent]
            flush_pending(target)
            key, val = top.group(1), top.group(2)
            if val == "" or val == "|":
                # block start: could be a nesting parent or a multi-line scalar.
                # If next non-empty line is indented, treat as parent.
                out[key] = {}
                current_parent = key
                pending_key = None
                pending_lines = []
            else:
                out[key] = strip_quotes(val)
                current_parent = None
        else:
            # continuation of a multi-line value
            if pending_key is not None:
                pending_lines.append(raw)
            elif raw.startswith((" ", "\t")) and current_parent is None:
                # stray indented line at top level — ignore
                continue
    flush_pending(out if current_parent is None else out[current_parent])

    # Promote nested metadata fields if useful
    md = out.get("metadata")
    if isinstance(md, dict):
        for k in ("version", "author", "category"):
            if k in md and k not in out:
                out[k] = md[k]
    return out


def parse_overlap_rules(path: Path) -> dict[str, str]:
    """Return {name: winner} from OVERLAP.md table rows."""
    if not path.exists():
        return {}
    rules: dict[str, str] = {}
    dash_only = re.compile(r"^-+$")
    for line in path.read_text().splitlines():
        if not line.startswith("|"):
            continue
        cols = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cols) < 2:
            continue
        name, winner = cols[0], cols[1]
        if not name or not winner:
            continue
        if name == "name" and winner == "winner":  # header row
            continue
        if dash_only.match(name) or dash_only.match(winner):  # separator
            continue
        rules[name] = winner
    return rules


def _normalize_bundle_source(src: Any) -> str:
    """Extract the relative path from a bundle source ref."""
    if isinstance(src, str):
        return src.lstrip("./")
    if isinstance(src, dict):
        p = src.get("path") or src.get("source") or ""
        return p.lstrip("./")
    return ""


def load_upstream_marketplace() -> tuple[list[dict[str, Any]], list[Path]]:
    """Return (rewritten bundle entries, canonical skill walk roots inside upstream/)."""
    if not UPSTREAM_MARKETPLACE.exists():
        return [], []
    data = json.loads(UPSTREAM_MARKETPLACE.read_text())
    bundles = data.get("plugins", [])
    rewritten = []
    roots: list[Path] = []
    for b in bundles:
        b = dict(b)
        rel = _normalize_bundle_source(b.get("source"))
        if rel:
            roots.append(UPSTREAM_DIR / rel)
            b["source"] = {"source": "./upstream/" + rel, "type": "directory"}
        rewritten.append(b)
    return rewritten, roots


def find_skills(roots: list[Path], max_depth: int | None = None) -> list[dict[str, Any]]:
    """Walk given roots for SKILL.md files and return entries with parsed frontmatter.

    Broken symlinks and unreadable files are skipped silently.
    Within each root, only follows real files (no symlinks) to avoid the
    `.gemini/skills/*` mirror-export build outputs in upstream.

    If `max_depth` is set, only SKILL.md files at exactly that many path-segments
    below `root` are accepted (e.g. max_depth=2 accepts root/<name>/SKILL.md and
    rejects deeper nesting). Used to keep staged-not-promoted content out of the
    catalog.
    """
    entries = []
    seen_paths: set[Path] = set()
    for root in roots:
        if not root.exists():
            continue
        for skill_md in root.rglob("SKILL.md"):
            if skill_md.is_symlink() or not skill_md.is_file():
                continue
            if max_depth is not None and len(skill_md.relative_to(root).parts) > max_depth:
                continue
            resolved = skill_md.resolve()
            if resolved in seen_paths:
                continue
            seen_paths.add(resolved)
            skill_dir = skill_md.parent
            try:
                text = skill_md.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            fm = parse_frontmatter(text)
            name = fm.get("name") or skill_dir.name
            if not name:
                continue
            rel = skill_dir.relative_to(ROOT).as_posix()
            entry = {
                "name": name,
                "source": {"source": "./" + rel, "type": "directory"},
                "description": fm.get("description", ""),
                "version": str(fm.get("version", "")),
                "author": fm.get("author", ""),
                "license": fm.get("license", ""),
                "category": fm.get("category", ""),
            }
            entry = {k: v for k, v in entry.items() if v not in ("", None, {})}
            entries.append(entry)
    return entries


def find_md_entries(root: Path, exclude_subdirs: set[Path] | None = None) -> list[dict[str, Any]]:
    """Walk root for *.md files (not SKILL.md) and return entries.

    `exclude_subdirs` is a set of directories to skip entirely. Use this to
    keep persona files out of the agent walk, for example. Meta filenames
    (README, TEMPLATE, etc.) are always skipped.
    """
    entries: list[dict[str, Any]] = []
    if not root.exists():
        return entries
    excluded = exclude_subdirs or set()
    for md in root.rglob("*.md"):
        if md.name in META_FILENAMES:
            continue
        if md.name == "SKILL.md":
            continue
        if md.is_symlink() or not md.is_file():
            continue
        if any(parent in excluded for parent in md.parents):
            continue
        try:
            text = md.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        fm = parse_frontmatter(text)
        # For agents/personas/commands use the file stem as the slug-name —
        # frontmatter `name` is treated as a display label only, so the
        # installable identifier stays URL-safe.
        name = md.stem
        if not name:
            continue
        rel = md.relative_to(ROOT).as_posix()
        display = fm.get("name") if fm.get("name") and fm.get("name") != name else ""
        description = fm.get("description", "")
        if display:
            description = f"{display}: {description}" if description else display
        entry = {
            "name": name,
            "source": {"source": "./" + rel, "type": "file"},
            "description": description,
            "version": str(fm.get("version", "")),
            "author": fm.get("author", ""),
            "license": fm.get("license", ""),
            "category": fm.get("category", ""),
        }
        entry = {k: v for k, v in entry.items() if v not in ("", None, {})}
        entries.append(entry)
    return entries


def dedup_by_name(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: dict[str, dict[str, Any]] = {}
    for e in entries:
        seen.setdefault(e["name"], e)
    return sorted(seen.values(), key=lambda e: e["name"])


def merge_with_overlap(upstream: list[dict[str, Any]], first_party: list[dict[str, Any]], rules: dict[str, str]) -> list[dict[str, Any]]:
    """Merge two lists keyed by name; first-party wins unless OVERLAP.md says otherwise.

    Within upstream, if a name appears multiple times the first occurrence wins
    (stable canonical paths come before mirrored copies in walk order).
    """
    upstream_by_name: dict[str, dict[str, Any]] = {}
    for e in upstream:
        upstream_by_name.setdefault(e["name"], e)
    fp_by_name: dict[str, dict[str, Any]] = {}
    for e in first_party:
        fp_by_name.setdefault(e["name"], e)
    all_names = set(upstream_by_name) | set(fp_by_name)
    out = []
    for name in sorted(all_names):
        winner = rules.get(name)
        if name in upstream_by_name and name in fp_by_name:
            if winner == "upstream":
                out.append(upstream_by_name[name])
            else:
                # default: ours wins
                out.append(fp_by_name[name])
        elif name in fp_by_name:
            out.append(fp_by_name[name])
        else:
            out.append(upstream_by_name[name])
    return out


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--verbose", "-v", action="store_true")
    ap.add_argument("--dry-run", action="store_true", help="print to stdout instead of writing")
    args = ap.parse_args(argv)

    rules = parse_overlap_rules(OVERLAP_PATH)
    if args.verbose:
        print(f"[overlap] {len(rules)} rule(s) loaded: {rules}", file=sys.stderr)

    bundles, upstream_roots = load_upstream_marketplace()
    # Bundle-internal SKILL.md files (under upstream/<bundle>/skills/...) are NOT
    # walked here — they install with their parent plugin. upstream_roots is
    # retained for forthcoming contains: enrichment.
    first_party_skills = find_skills([SKILLS_DIR], max_depth=2)
    personas = dedup_by_name(find_md_entries(PERSONAS_ROOT))
    agents = dedup_by_name(find_md_entries(AGENTS_ROOT, exclude_subdirs={PERSONAS_ROOT}))
    commands = dedup_by_name(find_md_entries(COMMANDS_ROOT))
    if args.verbose:
        print(f"[upstream] {len(bundles)} bundles", file=sys.stderr)
        print(f"[upstream] {len(personas)} personas, {len(agents)} agents, {len(commands)} commands", file=sys.stderr)
        print(f"[first-party] {len(first_party_skills)} SKILL.md (depth-capped)", file=sys.stderr)

    # OVERLAP.md merge path retained for forward-compat; with no upstream skill
    # candidates it is effectively a no-op for skills[] under the current scheme.
    skills = merge_with_overlap([], first_party_skills, rules)

    marketplace = {
        "name": "claude-skills-jesper",
        "owner": {"name": "flight505", "url": "https://github.com/flight505"},
        "description": "Curated Claude Code skills, agents, personas, and commands — vendored from alirezarezvani/claude-skills plus first-party additions.",
        "homepage": "https://github.com/flight505/claude-skills-jesper",
        "metadata": {
            "version": "0.1.0",
            "generated": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
            "upstream": {
                "repo": "alirezarezvani/claude-skills",
                "subtree_prefix": "upstream",
            },
            "counts": {
                "bundles": len(bundles),
                "skills": len(skills),
                "skills_first_party": len(first_party_skills),
                "agents": len(agents),
                "personas": len(personas),
                "commands": len(commands),
            },
        },
        "plugins": bundles,
        "skills": skills,
        "agents": agents,
        "personas": personas,
        "commands": commands,
    }

    body = json.dumps(marketplace, indent=2, ensure_ascii=False) + "\n"
    if args.dry_run:
        print(body)
        return 0
    OUT_PATH.write_text(body, encoding="utf-8")
    if args.verbose:
        print(f"[write] {OUT_PATH} ({len(body):,} bytes)", file=sys.stderr)
    print(f"marketplace.json regenerated: {len(bundles)} bundles + {len(skills)} skills")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
