# CLAUDE.md — claude-skills-jesper

Personal Claude Code skills marketplace. Vendors [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) via `git subtree` under `upstream/` and adds first-party skills under `skills/`.

## Critical paths

- `upstream/` — never hand-edit. Pull updates with `./scripts/sync-upstream.sh`.
- `skills/` — first-party only. Edit freely.
- `.claude-plugin/marketplace.json` — **generated**. Never hand-edit; run `python3 scripts/regenerate-marketplace.py`.

## Adding a first-party skill

1. Create `skills/<name>/SKILL.md` with required frontmatter (name, description, version, etc.)
2. Add an optional `pairs_with:` list (see below) to help the in-TUI chat suggest pairings
3. `python3 scripts/regenerate-marketplace.py`
4. `forge list --type skill | grep <name>` — verify it appears

### `pairs_with:` — pairing hints for the chat

When a catalog item has natural collaborators (a frontend-design skill that pairs with a design-system skill; a docs-skill that pairs with another docs-skill in a related domain), declare them in the frontmatter:

```yaml
---
name: frontend-learning
description: Builds interactive HTML explainers.
version: 0.1.0
pairs_with: frontend-design, design-md
---
```

Or, equivalently, as a YAML list:

```yaml
pairs_with:
  - frontend-design
  - design-md
```

Both shapes are parsed by `scripts/regenerate-marketplace.py` and surface as a `pairs_with: [...]` array on the entry in `marketplace.json`. The forge TUI's chat pane and the web `ItemChat` panel read this list and prepend the named items to their peer-suggestion set (replacing the same-type-first-10 heuristic when explicit pairs exist). Names must match other entries' `name:` exactly — a wrong name silently drops the hint, no error.

## Pulling upstream updates

```bash
./scripts/sync-upstream.sh
```

This runs `git subtree pull --squash` and regenerates `marketplace.json`. Preview changes first with `python3 scripts/upstream-changelog.py`.

## Type taxonomy (mirrors upstream)

| Type      | Purpose                  | Voice              |
|-----------|--------------------------|--------------------|
| skill     | How to execute a task    | Neutral            |
| agent     | What task to do          | Professional       |
| persona   | Who is thinking          | Personality-driven |
| command   | Slash-command shortcut   | Imperative         |
| bundle    | Group of the above       | n/a                |

## Install layer

Managed via [`forge`](https://github.com/flight505/forge). This repo is content + sync only — no CLI of its own.

## Doc-skill refresh daemons

Several skills (`claude-docs-skill`, `openrouter-docs-skill`, `warp-docs-skill`, `gemini-docs-skill`, `spark-docs-skill`, `nvidia-dgx-research`, `design-md`) ship `scripts/update-*.sh` that regenerate their `references/` content from upstream sources. The generated files are **not committed** — they're gitignored. To keep them fresh on a clone:

```bash
skills/_shared/install-refresh-daemons.sh           # install missing launchd daemons (macOS)
skills/_shared/install-refresh-daemons.sh --list    # preview without installing
skills/_shared/install-refresh-daemons.sh --force   # rewrite existing
skills/_shared/install-refresh-daemons.sh --uninstall
```

Each daemon fires immediately on first install (so a fresh clone has docs within seconds) and then weekly on Sundays at 04:00 local. macOS-only (launchd); Linux users should map the printed commands to cron.

## Source manifests

Each first-party skill ships a `_source.yaml` declaring where it came from and how it stays current. `agents/` carries one manifest covering all first-party agents. `scripts/check-sources.py` reads every manifest and reports which items have updates available.

Four kinds:

| `kind` | meaning | refresh method |
|---|---|---|
| `original` | Hand-edited content I author | none |
| `docs` | Snapshot of an upstream documentation site I maintain | launchd weekly (see daemon section above) |
| `repo-mirror` | Snapshot of someone else's published artifact (npm package, GitHub repo, …) | launchd weekly; check-sources also probes the origin for newer versions |
| `subtree` | Vendored marketplace pulled via `git subtree` | manual — `./scripts/sync-upstream.sh` |

Schema (all fields optional unless noted; minimal `original` form is just `kind: original`):

```yaml
# skills/<name>/_source.yaml
kind: docs                                 # required: original | docs | repo-mirror | subtree
origin: https://platform.claude.com/...    # source URL or URI (npm:pkg, github:org/repo@ref)
version: "0.6.20"                          # for repo-mirror: the vendored version
refresh:
  method: launchd                          # none | manual | launchd | subtree
  script: scripts/update-cli-docs.sh       # relative path to the refresh script
  schedule: "Sunday 04:00 weekly"          # human-readable cadence
notes: "Tier-1/2/3 doc snapshot from platform.claude.com"
```

Adding a new skill? Drop a `_source.yaml` next to its `SKILL.md` with at minimum `kind:`. `original` is the default if you skip the manifest entirely, but writing it explicitly future-proofs `scripts/check-sources.py`.

## Overlap rules

When upstream and first-party have the same skill name:
- **Default: ours wins** (skills/ takes precedence)
- Exceptions tracked in `OVERLAP.md`
- Confirmed exception: `deepwiki` — use upstream's

## Conventions

- Python: stdlib only. No pip dependencies in `scripts/`.
- Run `python3 scripts/regenerate-marketplace.py` after any change to `skills/` or `upstream/`.
- Commit `marketplace.json` after regeneration.
