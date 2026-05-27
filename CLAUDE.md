# CLAUDE.md — claude-skills-jesper

Personal Claude Code skills marketplace. The bulk of the catalog (~130 of 143 items — all plugins, all commands, all personas, and most agents) is vendored from [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) under `upstream/` via `git subtree`. A small first-party layer under `skills/` and `agents/` (~13 items) sits on top.

Current composition (regenerate-marketplace.py output):

| Type     | first-party | upstream | total |
|----------|------------:|---------:|------:|
| skills   | 10          | 0        | 10    |
| plugins  | 0           | 61       | 61    |
| agents   | 3           | 24       | 27    |
| commands | 0           | 38       | 38    |
| personas | 0           | 7        | 7     |

When asked to "pick something from the catalog" or "audit the marketplace," sample both layers — `upstream/` is the surface area, not just an external dependency.

## Critical paths

- `upstream/` — vendored catalog; source of all plugins/commands/personas and most agents. Never hand-edit; pull updates with `./scripts/sync-upstream.sh`.
- `skills/` — first-party skills. Edit freely.
- `agents/` — first-party agents (3 today). Edit freely.
- `.claude-plugin/marketplace.json` — **generated**. Never hand-edit; run `python3 scripts/regenerate-marketplace.py`.

## Adding a first-party skill

1. Create `skills/<name>/SKILL.md` with required frontmatter (name, description, version, etc.)
2. Add an optional `pairs_with:` list (see below) to help the in-TUI chat suggest pairings
3. `python3 scripts/regenerate-marketplace.py`
4. `forge list --type skill | grep <name>` — verify it appears

### `pairs_with:` — pairing hints for the chat

When a catalog item has natural collaborators, declare them in the frontmatter as either a comma-separated string or a YAML list:

```yaml
pairs_with: frontend-design, design-md
# or
pairs_with:
  - frontend-design
  - design-md
```

`scripts/regenerate-marketplace.py` normalises both into a `pairs_with: [...]` array on the marketplace entry. The forge TUI's chat pane and the web `ItemChat` panel prepend these to their peer-suggestion set (replacing the same-type-first-10 heuristic when explicit pairs exist). Names must match other entries' `name:` exactly — a wrong name silently drops the hint.

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

Catalog items install into the Claude Code CLI by default. To target Claude Cowork instead, pass `--surface cowork` (or pick the cowork surface in `forge tui` / `forge serve`). Cowork's loader only understands plugins, so non-plugin items are auto-wrapped at install time.

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

## Integrating a third-party repo

When a third-party skill/plugin/agent repo looks worth adopting, the informal workflow is:

1. `cd` into this repo and start a Claude Code session
2. Paste the git URL and ask Claude to review the repo and propose how to integrate it
3. Decide the type (skill/plugin/agent/persona/command) and the provenance kind (`original`/`docs`/`repo-mirror`/`subtree` — see Source manifests above)
4. Copy or subtree-pull the content into the right destination:
   - Individual skill → `skills/<name>/` with a `SKILL.md`
   - Agent → `agents/<name>.md`
   - If tracking upstream updates matters → prefer `git subtree add` and document in `OVERLAP.md`
5. Add a `_source.yaml` with `kind: repo-mirror` (or `subtree` if pulling via git subtree) and the `origin:` URI
6. Run `python3 scripts/regenerate-marketplace.py` and verify it appears in the catalog
7. `forge install <name>` smoke-test from a fresh session

No dedicated skill is needed for this workflow — starting a Claude session with the URL and this CLAUDE.md loaded is sufficient.

## Overlap rules

When upstream and first-party have the same skill name:
- **Default: ours wins** (skills/ takes precedence)
- Exceptions tracked in `OVERLAP.md`
- Confirmed exception: `deepwiki` — use upstream's

## Conventions

- Python: stdlib only. No pip dependencies in `scripts/`.
- Run `python3 scripts/regenerate-marketplace.py` after any change to `skills/` or `upstream/`.
- Commit `marketplace.json` after regeneration.
