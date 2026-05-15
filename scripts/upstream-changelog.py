#!/usr/bin/env python3
"""Show what would change in `upstream/` if we synced against a given git ref.

Compares the current state of `upstream/` to a remote ref (default: the last
fetched `upstream-skills/main`) and lists added / removed / modified SKILL.md
directories. Uses `git diff --name-status` under the hood — read-only.

Usage:
    scripts/upstream-changelog.py
    scripts/upstream-changelog.py --against upstream-skills/main
    scripts/upstream-changelog.py --against v2.2.3 --verbose
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PREFIX = "upstream/"


def git(*args: str) -> str:
    return subprocess.check_output(["git", "-C", str(ROOT), *args], text=True)


def remote_tree_paths(ref: str) -> set[str]:
    """List every file path under the remote ref. Paths are unprefixed (relative to upstream root)."""
    try:
        out = git("ls-tree", "-r", "--name-only", ref)
    except subprocess.CalledProcessError as e:
        print(f"error: cannot read ref {ref!r}: {e}", file=sys.stderr)
        sys.exit(2)
    return set(out.splitlines())


def local_tree_paths() -> set[str]:
    """Files currently tracked under upstream/, paths relative to upstream/.

    Uses `git ls-files` so the comparison is symmetrical with the remote-side
    `git ls-tree`. Both ignore unstaged/untracked files; both include broken
    symlinks (which exist in the upstream repo's git tree but resolve to
    nothing on disk after squash). This avoids false-positive diffs.
    """
    try:
        out = git("ls-files", PREFIX)
    except subprocess.CalledProcessError:
        return set()
    return {p[len(PREFIX):] for p in out.splitlines() if p.startswith(PREFIX)}


def directories_of(paths: set[str], marker: str = "SKILL.md") -> set[str]:
    """Return the set of directories that contain `marker`. Dirs relative to upstream/."""
    return {p[: -len(marker) - 1] for p in paths if p.endswith("/" + marker) or p == marker}


def classify(local: set[str], remote: set[str]) -> dict[str, list[str]]:
    added = sorted(remote - local)
    removed = sorted(local - remote)
    return {"added": added, "removed": removed, "common": sorted(local & remote)}


def short(s: str, n: int = 70) -> str:
    return s if len(s) <= n else s[: n - 1] + "…"


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--against", default="upstream-skills/main",
                    help="git ref to compare against (default: upstream-skills/main)")
    ap.add_argument("--verbose", "-v", action="store_true")
    args = ap.parse_args(argv)

    remote_paths = remote_tree_paths(args.against)
    local_paths = local_tree_paths()

    if not remote_paths:
        print(f"no files under ref {args.against}", file=sys.stderr)
        return 1

    # Skill-level diff (SKILL.md directories)
    skill_diff = classify(directories_of(local_paths), directories_of(remote_paths))

    # File-level total counts (informational)
    added_files = sorted(remote_paths - local_paths)
    removed_files = sorted(local_paths - remote_paths)

    print(f"comparing upstream/ vs {args.against}")
    print(f"  files added:   {len(added_files):4d}")
    print(f"  files removed: {len(removed_files):4d}")
    print(f"  skills added:    {len(skill_diff['added']):4d}")
    print(f"  skills removed:  {len(skill_diff['removed']):4d}")
    print()

    by_bundle: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for d in skill_diff["added"]:
        by_bundle[d.split("/", 1)[0]].append(("+", d))
    for d in skill_diff["removed"]:
        by_bundle[d.split("/", 1)[0]].append(("-", d))

    if not by_bundle:
        print("no skill-level changes.")
        return 0

    for bundle, rows in sorted(by_bundle.items()):
        print(f"[{bundle}]")
        for sign, d in rows:
            print(f"  {sign} {short(d)}")
        print()

    if args.verbose and added_files:
        print(f"--- new files (first 20) ---")
        for f in added_files[:20]:
            print(f"  + {short(f)}")
    if args.verbose and removed_files:
        print(f"--- removed files (first 20) ---")
        for f in removed_files[:20]:
            print(f"  - {short(f)}")

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
