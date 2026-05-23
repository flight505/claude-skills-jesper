#!/usr/bin/env python3
"""Check every first-party item's source for available updates.

Walks every `_source.yaml` under `skills/*/` and at the repo root (`agents/`),
groups items by `kind`, and probes the appropriate origin per kind:

  - original      → no probe; report as static
  - docs          → check `references/` mtime, flag if older than --stale-days
  - repo-mirror   → query the origin (currently: npm registry) for a newer
                    version than `version:` declared in the manifest
  - subtree       → not represented as a manifest; the upstream tree is
                    probed separately at the bottom of the report via
                    `git fetch upstream-skills main` + commit count

Read-only by default. Pass `--fix` to actually run the refresh action per
stale item:

  - docs:        `launchctl kickstart -k gui/$UID com.flight505.<short>-refresh`
  - repo-mirror: run the script declared in `refresh.script`
  - subtree:     `./scripts/sync-upstream.sh`

Stdlib only — no pip dependencies, per the project's Python convention.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
AGENTS_DIR = ROOT / "agents"


# ── minimal YAML reader ───────────────────────────────────────────────────────
# Stdlib has no yaml, so parse the small subset the manifests actually use:
# top-level scalar keys, top-level list-of-scalars, one nested dict.
def parse_yaml(text: str) -> dict:
    """Parse a tiny subset of YAML: scalars, lists, and one-level nested maps.
    Sufficient for `_source.yaml`. Not a general-purpose parser.
    """
    out: dict = {}
    current_parent: str | None = None
    current_list_key: str | None = None

    def parse_scalar(raw: str) -> str:
        raw = raw.strip()
        if (len(raw) >= 2) and (raw[0] == raw[-1]) and (raw[0] in ('"', "'")):
            return raw[1:-1]
        return raw

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        # nested key (4+ leading spaces under a `parent:` line that opened a map)
        if line.startswith("  ") and current_parent is not None and not line.lstrip().startswith("-"):
            m = re.match(r"^\s+([A-Za-z_][\w-]*)\s*:\s*(.*)$", line)
            if m:
                k, v = m.group(1), m.group(2)
                if v == "":
                    # nested dict that opens with no value — rare in our manifests, ignore
                    continue
                out.setdefault(current_parent, {})[k] = parse_scalar(v)
                continue
        # list item under current_list_key
        if line.lstrip().startswith("- ") and current_list_key is not None:
            item = parse_scalar(line.lstrip()[2:])
            out.setdefault(current_list_key, []).append(item)
            continue
        # top-level key
        m = re.match(r"^([A-Za-z_][\w-]*)\s*:\s*(.*)$", line)
        if not m:
            continue
        k, v = m.group(1), m.group(2)
        current_parent = None
        current_list_key = None
        if v == "":
            # could open either a list or a nested map — defer; next line decides
            current_parent = k
            current_list_key = k
            continue
        out[k] = parse_scalar(v)
    return out


# ── manifest discovery ────────────────────────────────────────────────────────
def load_manifests() -> list[tuple[Path, dict]]:
    """Return [(item_dir, manifest_dict), …] for every _source.yaml found.

    Item dirs are reported relative to ROOT. For `agents/_source.yaml` the
    item dir is `agents/` itself.
    """
    out: list[tuple[Path, dict]] = []
    for d in sorted(SKILLS_DIR.iterdir() if SKILLS_DIR.exists() else []):
        if d.name.startswith("_"):
            continue
        mf = d / "_source.yaml"
        if mf.exists():
            try:
                out.append((d, parse_yaml(mf.read_text(encoding="utf-8"))))
            except Exception as e:
                out.append((d, {"_parse_error": str(e)}))
    agents_mf = AGENTS_DIR / "_source.yaml"
    if agents_mf.exists():
        try:
            out.append((AGENTS_DIR, parse_yaml(agents_mf.read_text(encoding="utf-8"))))
        except Exception as e:
            out.append((AGENTS_DIR, {"_parse_error": str(e)}))
    return out


# ── per-kind probes ───────────────────────────────────────────────────────────
class ProbeResult:
    """One row in the report."""
    def __init__(self, name: str, kind: str, status: str, detail: str = "", fix_cmd: list[str] | None = None):
        self.name = name
        self.kind = kind
        self.status = status   # "ok" | "stale" | "update-available" | "unknown" | "error"
        self.detail = detail
        self.fix_cmd = fix_cmd or []


def probe_original(item_dir: Path, _manifest: dict) -> ProbeResult:
    return ProbeResult(item_dir.name, "original", "ok", "static (no external refresh)")


def probe_docs(item_dir: Path, manifest: dict, stale_days: int) -> ProbeResult:
    refs = item_dir / "references"
    label = launchd_label_for(item_dir, manifest)
    if not refs.exists():
        return ProbeResult(item_dir.name, "docs", "unknown",
                           f"references/ dir missing — daemon {label} may never have fired")
    # Newest mtime under references/ tells us last refresh time.
    newest = 0.0
    for p in refs.rglob("*"):
        if p.is_file() and not p.name.startswith("."):
            newest = max(newest, p.stat().st_mtime)
    if newest == 0:
        fix = ["launchctl", "kickstart", "-k", f"gui/{os.getuid()}/{label}"]
        return ProbeResult(item_dir.name, "docs", "stale",
                           f"references/ empty — fire {label} to populate", fix)
    age_sec = time.time() - newest
    age_days = age_sec / 86400
    if age_days <= stale_days:
        return ProbeResult(item_dir.name, "docs", "ok", f"last refreshed {age_days:.1f}d ago")
    # Stale — kickstart the daemon.
    fix = ["launchctl", "kickstart", "-k", f"gui/{os.getuid()}/{label}"]
    return ProbeResult(item_dir.name, "docs", "stale",
                       f"last refreshed {age_days:.1f}d ago — daemon {label}", fix)


def launchd_label_for(item_dir: Path, manifest: dict) -> str:
    """Derive the launchd label for a docs/repo-mirror item. Prefers a label
    embedded in the manifest's `refresh.schedule` (the convention used in the
    backfill: "Sunday 04:00 weekly (com.flight505.<short>-refresh)"), and
    falls back to the deterministic naming rule from install-refresh-daemons.sh
    (strip `-skill` suffix, prefix with `com.flight505.`, suffix `-refresh`).
    """
    refresh = manifest.get("refresh")
    if isinstance(refresh, dict):
        schedule = refresh.get("schedule", "")
        if isinstance(schedule, str):
            m = re.search(r"com\.[\w.\-]+-refresh", schedule)
            if m:
                return m.group(0)
    short = item_dir.name.removesuffix("-skill")
    return f"com.flight505.{short}-refresh"


def probe_repo_mirror(item_dir: Path, manifest: dict) -> ProbeResult:
    origin = manifest.get("origin", "")
    local_version = manifest.get("version", "")
    if origin.startswith("npm:"):
        pkg = origin[4:]
        latest = npm_latest(pkg)
        if latest is None:
            return ProbeResult(item_dir.name, "repo-mirror", "unknown", f"could not query npm registry for {pkg}")
        if local_version == latest:
            return ProbeResult(item_dir.name, "repo-mirror", "ok", f"npm:{pkg} pinned at {local_version} (matches latest)")
        # Update available. Fix command runs the manifest's refresh script.
        refresh = manifest.get("refresh", {})
        script = refresh.get("script", "")
        fix: list[str] = []
        if script:
            fix = ["bash", str(item_dir / script)]
        return ProbeResult(item_dir.name, "repo-mirror", "update-available", f"npm:{pkg} local {local_version} → latest {latest}", fix)
    return ProbeResult(item_dir.name, "repo-mirror", "unknown", f"no probe for origin {origin!r}")


def npm_latest(pkg: str) -> str | None:
    """Hit registry.npmjs.org for the `latest` dist-tag. None on any failure."""
    url = f"https://registry.npmjs.org/{pkg}/latest"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "claude-skills-jesper/check-sources"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.load(resp)
            return data.get("version")
    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError, TimeoutError):
        return None


def probe_subtree() -> ProbeResult:
    """The upstream/ subtree gets its own probe — no manifest. Counts commits
    in upstream-skills/main not yet squashed into our tree."""
    # Need the remote configured. If not, skip.
    try:
        subprocess.run(
            ["git", "-C", str(ROOT), "remote", "get-url", "upstream-skills"],
            check=True, capture_output=True,
        )
    except subprocess.CalledProcessError:
        return ProbeResult("upstream", "subtree", "unknown", "remote `upstream-skills` not configured — run sync-upstream.sh once")

    try:
        subprocess.run(
            ["git", "-C", str(ROOT), "fetch", "upstream-skills", "main", "--quiet"],
            check=True, capture_output=True, timeout=15,
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        return ProbeResult("upstream", "subtree", "error", f"git fetch failed: {e}")

    # Find the last subtree squash. They're created by `git subtree pull --squash`
    # with subject "Squashed 'upstream/' changes from <old>..<new>". Grab the
    # latest one and pull the <new> SHA — that's our high-water mark.
    log = subprocess.run(
        ["git", "-C", str(ROOT), "log", "--grep=^Squashed 'upstream/' changes from", "--format=%s", "-1"],
        capture_output=True, text=True,
    )
    m = re.search(r"\.\.([0-9a-f]+)", log.stdout)
    if not m:
        return ProbeResult("upstream", "subtree", "unknown", "no subtree squash commit found in history")
    high_water = m.group(1)

    count = subprocess.run(
        ["git", "-C", str(ROOT), "rev-list", "--count", f"{high_water}..upstream-skills/main"],
        capture_output=True, text=True,
    )
    n = int(count.stdout.strip() or "0")
    if n == 0:
        return ProbeResult("upstream", "subtree", "ok", "in sync with upstream-skills/main")
    fix = ["./scripts/sync-upstream.sh"]
    return ProbeResult("upstream", "subtree", "update-available", f"{n} commits ahead — preview with scripts/upstream-changelog.py", fix)


# ── report rendering ──────────────────────────────────────────────────────────
STATUS_COLOR = {
    "ok": "\033[2m",                 # dim
    "stale": "\033[33m",             # yellow
    "update-available": "\033[33m",  # yellow
    "unknown": "\033[2m",            # dim
    "error": "\033[31m",             # red
}
RESET = "\033[0m"


def render(results: list[ProbeResult], use_color: bool) -> str:
    by_kind: dict[str, list[ProbeResult]] = {}
    for r in results:
        by_kind.setdefault(r.kind, []).append(r)
    lines: list[str] = []
    order = ["original", "docs", "repo-mirror", "subtree"]
    for kind in order:
        if kind not in by_kind:
            continue
        lines.append(f"\n[{kind}]")
        for r in sorted(by_kind[kind], key=lambda x: x.name):
            color = STATUS_COLOR.get(r.status, "") if use_color else ""
            reset = RESET if use_color else ""
            tag = r.status.upper().ljust(18)
            lines.append(f"  {r.name:32s}  {color}{tag}{reset} {r.detail}")
    return "\n".join(lines)


# ── --fix runner ──────────────────────────────────────────────────────────────
def run_fix(results: list[ProbeResult]) -> int:
    """Run the fix command for every result that needs an update. Returns
    the number of commands that exited non-zero."""
    failures = 0
    for r in results:
        if r.status not in ("stale", "update-available"):
            continue
        if not r.fix_cmd:
            print(f"  [skip] {r.name}: no fix command available", file=sys.stderr)
            continue
        print(f"\n[fix] {r.name}: {' '.join(r.fix_cmd)}", file=sys.stderr)
        try:
            res = subprocess.run(r.fix_cmd, cwd=ROOT, check=False)
            if res.returncode != 0:
                print(f"  [fail] {r.name} exited {res.returncode}", file=sys.stderr)
                failures += 1
        except FileNotFoundError as e:
            print(f"  [fail] {r.name}: {e}", file=sys.stderr)
            failures += 1
    return failures


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--stale-days", type=int, default=10,
                   help="Flag docs items whose references/ are older than this (default: 10).")
    p.add_argument("--fix", action="store_true",
                   help="Run the appropriate refresh action for every stale / update-available item.")
    p.add_argument("--no-color", action="store_true", help="Disable ANSI colour in the report.")
    p.add_argument("--no-subtree", action="store_true", help="Skip the upstream-subtree probe (faster; offline-safe).")
    args = p.parse_args()

    use_color = (not args.no_color) and sys.stdout.isatty()
    results: list[ProbeResult] = []

    for item_dir, manifest in load_manifests():
        if "_parse_error" in manifest:
            results.append(ProbeResult(item_dir.name, "?", "error", f"manifest parse failed: {manifest['_parse_error']}"))
            continue
        kind = manifest.get("kind", "original")
        if kind == "original":
            results.append(probe_original(item_dir, manifest))
        elif kind == "docs":
            results.append(probe_docs(item_dir, manifest, args.stale_days))
        elif kind == "repo-mirror":
            results.append(probe_repo_mirror(item_dir, manifest))
        else:
            results.append(ProbeResult(item_dir.name, kind, "unknown", f"no probe for kind {kind!r}"))

    if not args.no_subtree:
        results.append(probe_subtree())

    print(render(results, use_color))

    needs_update = sum(1 for r in results if r.status in ("stale", "update-available"))
    if needs_update == 0:
        print(f"\nall sources fresh ({len(results)} items checked)" if not use_color
              else f"\n\033[32mall sources fresh\033[0m ({len(results)} items checked)")
    else:
        print(f"\n{needs_update} item(s) need attention. Re-run with --fix to refresh them automatically.")

    if args.fix:
        failures = run_fix(results)
        print(f"\nfix run complete; {failures} command(s) failed" if failures else "\nfix run complete; all refreshes triggered")
        return 1 if failures else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
