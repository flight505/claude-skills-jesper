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

# First-party agents live at the repo root (./agents/), mirroring how
# first-party skills live at ./skills/. Discovered separately from upstream
# agents and merged into the same agents[] array (first-party wins on name
# collision via merge_with_overlap).
FIRST_PARTY_AGENTS_DIR = ROOT / "agents"

# .md filenames we never treat as installable content.
META_FILENAMES = {"README.md", "TEMPLATE.md", "CHANGELOG.md", "CLAUDE.md", "GEMINI.md", "AGENTS.md"}

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*(?:\n|$)", re.DOTALL)
TOP_KEY_RE = re.compile(r"^([a-zA-Z_][\w-]*)\s*:\s*(.*?)\s*$")
NESTED_KEY_RE = re.compile(r"^[ \t]+([a-zA-Z_][\w-]*)\s*:\s*(.*?)\s*$")
LIST_DASH_RE = re.compile(r"^\s+-\s+(.+?)\s*$")


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
        # `key:\n  - item\n  - item` — list of scalars under the current parent.
        # First dash promotes the parent from {} to []; subsequent dashes append.
        list_item = LIST_DASH_RE.match(raw) if current_parent is not None else None
        if list_item and current_parent is not None:
            parent_key: str = current_parent  # narrow for type checker
            flush_pending(target_now if isinstance(target_now, dict) else {})
            if isinstance(out.get(parent_key), dict) and not out[parent_key]:
                out[parent_key] = []
            if isinstance(out.get(parent_key), list):
                out[parent_key].append(strip_quotes(list_item.group(1)))
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
    # Normalize pairs_with to a clean list[str] regardless of whether the
    # frontmatter used `pairs_with: a, b, c` or YAML-list `pairs_with:\n - a\n - b`.
    pw = out.get("pairs_with")
    if isinstance(pw, str):
        out["pairs_with"] = [s.strip() for s in pw.split(",") if s.strip()]
    elif isinstance(pw, list):
        out["pairs_with"] = [str(s).strip() for s in pw if str(s).strip()]
    elif pw is not None:
        # malformed shape (dict, etc.) — drop quietly
        out.pop("pairs_with", None)
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


def _nearest_declared(path: Path, declared: set[Path]) -> Path | None:
    """Walk `path` and its parents; return the first one in `declared`."""
    for ancestor in (path, *path.parents):
        if ancestor in declared:
            return ancestor
    return None


def enumerate_bundle_contents(bundle_dir: Path, declared_source_dirs: set[Path]) -> dict[str, list[str]]:
    """Return {skills, agents, commands, sub_plugins} living inside `bundle_dir`.

    Decoration for discovery — forge ignores unknown Entry fields. Identifiers
    are directory names (stable, slug-safe), not frontmatter `name`.

    "Nearest declared bundle" filtering: an item inside a sub-plugin that is
    itself declared as a top-level plugin in the upstream marketplace belongs
    to that sub-plugin, not to `bundle_dir`. Items inside *undeclared* sub-dirs
    bubble up to the nearest declared ancestor.
    """
    own = bundle_dir.resolve()
    if not own.exists():
        return {}

    buckets: dict[str, set[str]] = {"skills": set(), "agents": set(), "commands": set(), "sub_plugins": set()}

    # Skills: every SKILL.md whose nearest declared bundle is `own`.
    for skill_md in own.rglob("SKILL.md"):
        if skill_md.is_symlink() or not skill_md.is_file():
            continue
        if _nearest_declared(skill_md.parent.resolve(), declared_source_dirs) != own:
            continue
        buckets["skills"].add(skill_md.parent.name)

    # Agents/commands: only inside the bundle's own agents/ or commands/ subtree.
    for kind, dirname in (("agents", "agents"), ("commands", "commands")):
        sub = own / dirname
        if not sub.exists():
            continue
        for md in sub.rglob("*.md"):
            if md.is_symlink() or not md.is_file():
                continue
            if md.name in META_FILENAMES or md.name == "SKILL.md":
                continue
            if _nearest_declared(md.parent.resolve(), declared_source_dirs) != own:
                continue
            buckets[kind].add(md.stem)

    # Sub-plugins: nested .claude-plugin/plugin.json (not own) whose containing
    # dir is NOT itself declared top-level, AND whose nearest declared ancestor
    # is `own` (so it lands in the right parent if double-nested).
    own_plugin_json = (own / ".claude-plugin" / "plugin.json").resolve()
    for pj in own.rglob(".claude-plugin/plugin.json"):
        if pj.resolve() == own_plugin_json:
            continue
        plugin_dir = pj.parent.parent.resolve()
        if plugin_dir in declared_source_dirs:
            continue
        if _nearest_declared(plugin_dir, declared_source_dirs) != own:
            continue
        buckets["sub_plugins"].add(plugin_dir.name)

    return {k: sorted(v) for k, v in buckets.items() if v}


def load_upstream_marketplace() -> tuple[list[dict[str, Any]], set[Path]]:
    """Return (enriched bundle entries, resolved declared-bundle dirs).

    Each returned bundle gets a `contains:` field listing its constituent
    skills/agents/commands/sub-plugins (sub-plugins that are themselves
    declared at top level are intentionally excluded — they appear in plugins[]
    in their own right and would otherwise be listed twice).

    The declared-bundle-dirs set is exposed so a caller (e.g. orphan-bundle
    detection) can tell whether an arbitrary upstream/<dir> is already known.
    """
    if not UPSTREAM_MARKETPLACE.exists():
        return [], set()
    data = json.loads(UPSTREAM_MARKETPLACE.read_text())
    bundles_raw = data.get("plugins", [])

    # Pass 1: resolve every declared bundle source so contents/sub-plugin
    # filtering can know which dirs belong to other declared plugins.
    bundle_dirs: list[tuple[dict[str, Any], Path]] = []
    declared_source_dirs: set[Path] = set()
    for b in bundles_raw:
        rel = _normalize_bundle_source(b.get("source"))
        if not rel:
            continue
        bdir = (UPSTREAM_DIR / rel).resolve()
        bundle_dirs.append((dict(b), bdir))
        declared_source_dirs.add(bdir)

    # Pass 2: rewrite source ref + attach contains. Plugin sources must use
    # the canonical Claude Code shape — a bare string for relative paths —
    # not the {source, type} object forge previously emitted. The object
    # form was forge-internal metadata that Claude Code's plugin loader
    # rejects with "source type your Claude Code version does not support",
    # which silently broke `claude plugin install` for everything in this
    # marketplace.
    rewritten: list[dict[str, Any]] = []
    for b, bdir in bundle_dirs:
        rel = bdir.relative_to(UPSTREAM_DIR).as_posix()
        b["source"] = "./upstream/" + rel
        contents = enumerate_bundle_contents(bdir, declared_source_dirs)
        if contents:
            b["contains"] = contents
        rewritten.append(b)
    return rewritten, declared_source_dirs


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
                "pairs_with": fm.get("pairs_with") or [],
            }
            entry = {k: v for k, v in entry.items() if v not in ("", None, [], {})}
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
            "pairs_with": fm.get("pairs_with") or [],
        }
        entry = {k: v for k, v in entry.items() if v not in ("", None, [], {})}
        entries.append(entry)
    return entries


def find_orphan_bundles(declared_source_dirs: set[Path]) -> list[dict[str, Any]]:
    """Detect bundle-level plugin.json files not declared in upstream marketplace.

    Walks only depth-2 dirs (upstream/<dir>/.claude-plugin/plugin.json). Nested
    sub-plugins are handled separately via enumerate_bundle_contents.

    Each orphan is auto-included with a stderr warning so a stray dropped-in
    plugin.json doesn't silently leak — and so an intentional case like
    compliance-os (present but not yet declared upstream) shows up in the
    catalog without manual intervention.
    """
    orphans: list[dict[str, Any]] = []
    for child in sorted(UPSTREAM_DIR.iterdir()):
        if not child.is_dir() or child.name.startswith("."):
            continue
        plugin_json = child / ".claude-plugin" / "plugin.json"
        if not plugin_json.is_file():
            continue
        if child.resolve() in declared_source_dirs:
            continue
        try:
            data = json.loads(plugin_json.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"[orphan] skipping {child.name}: unreadable plugin.json ({exc})", file=sys.stderr)
            continue
        name = data.get("name") or child.name
        entry: dict[str, Any] = {
            "name": name,
            "source": "./upstream/" + child.name,
        }
        for key in ("description", "version", "author", "homepage", "repository", "license", "category", "keywords"):
            val = data.get(key)
            if val not in ("", None, [], {}):
                entry[key] = val
        contents = enumerate_bundle_contents(child, declared_source_dirs | {child.resolve()})
        if contents:
            entry["contains"] = contents
        print(f"[orphan] auto-included plugin: {name} (./upstream/{child.name})", file=sys.stderr)
        orphans.append(entry)
    return orphans


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

    bundles, declared_source_dirs = load_upstream_marketplace()
    orphan_bundles = find_orphan_bundles(declared_source_dirs)
    plugins = bundles + orphan_bundles
    # Bundle-internal SKILL.md files (under upstream/<bundle>/skills/...) are
    # NOT walked here — they install with their parent plugin and are listed
    # under that plugin's contains: field (added inside load_upstream_marketplace).
    first_party_skills = find_skills([SKILLS_DIR], max_depth=2)
    personas = dedup_by_name(find_md_entries(PERSONAS_ROOT))
    upstream_agents = dedup_by_name(find_md_entries(AGENTS_ROOT, exclude_subdirs={PERSONAS_ROOT}))
    first_party_agents = dedup_by_name(find_md_entries(FIRST_PARTY_AGENTS_DIR))
    commands = dedup_by_name(find_md_entries(COMMANDS_ROOT))
    if args.verbose:
        print(f"[upstream] {len(bundles)} declared + {len(orphan_bundles)} orphan = {len(plugins)} plugins", file=sys.stderr)
        print(f"[upstream] {len(personas)} personas, {len(upstream_agents)} agents, {len(commands)} commands", file=sys.stderr)
        print(f"[first-party] {len(first_party_skills)} SKILL.md, {len(first_party_agents)} agent(s)", file=sys.stderr)

    # OVERLAP.md merge path retained for forward-compat; with no upstream skill
    # candidates it is effectively a no-op for skills[] under the current scheme.
    skills = merge_with_overlap([], first_party_skills, rules)
    agents = merge_with_overlap(upstream_agents, first_party_agents, rules)

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
                "plugins": len(plugins),
                "plugins_declared": len(bundles),
                "plugins_orphan": len(orphan_bundles),
                "skills": len(skills),
                "skills_first_party": len(first_party_skills),
                "agents": len(agents),
                "personas": len(personas),
                "commands": len(commands),
            },
        },
        "plugins": plugins,
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
    print(f"marketplace.json regenerated: {len(plugins)} plugins + {len(skills)} skills")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
