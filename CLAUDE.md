# CLAUDE.md — claude-skills-jesper

Personal Claude Code skills marketplace. The bulk of the catalog (most plugins, all commands, all personas, and most agents) is vendored from [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) under `upstream/` via `git subtree`. A small first-party layer under `skills/`, `agents/`, and `plugins/` sits on top — roughly 14 first-party items versus ~130 from upstream.

Composition as of 2026-05-30 (re-run `python3 scripts/regenerate-marketplace.py` to refresh):

| Type     | first-party | upstream | total |
|----------|------------:|---------:|------:|
| skills   | 10          | 0        | 10    |
| plugins  | 1           | 64       | 65    |
| agents   | 3           | 24       | 27    |
| commands | 0           | 38       | 38    |
| personas | 0           | 7        | 7     |

**Discovery vs. maintenance — read this first.** To *find or use* a catalog item (pick one, audit the marketplace, suggest, install), go through `forge` — run `forge guide` (or `forge agent guide` for JSON) to learn how. Forge presents upstream + first-party as one unified surface, so you never reason about folders; discover via `forge search`/`list`/`show`/`agent search`. **Do not grep `skills/` or `upstream/` to discover what exists** — `skills/` holds only ~10 items and you'll silently miss the ~130 in `upstream/`. The folder paths documented below are for *maintaining* this repo (editing, adding, syncing), not for finding catalog items.

## Critical paths (maintenance only — see discovery note above)

- `upstream/` — vendored catalog; source of all plugins/commands/personas and most agents. Never hand-edit; pull updates with `./scripts/sync-upstream.sh`.
- `skills/` — first-party skills. Edit freely.
- `agents/` — first-party agents (3 today). Edit freely.
- `plugins/` — first-party plugins (1 today). Edit freely; each needs `.claude-plugin/plugin.json`. The first-party analogue of `upstream/` bundles.
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

## Adding a first-party plugin

Plugins are multi-component bundles (a `.claude-plugin/plugin.json` plus any of `agents/`, `skills/`, `commands/`, `hooks/`). All but one come from `upstream/`; first-party plugins live at the repo root under `plugins/`, the analogue of `skills/` and `agents/`.

1. Create `plugins/<name>/` with a `.claude-plugin/plugin.json` (required: `name`, `description`; optional `version`, `author`, `repository`, `license`, `keywords`). Drop bundled `agents/`, `skills/`, etc. alongside it.
2. Add a `_source.yaml` (`kind: repo-mirror` for a vendored third-party plugin, `original` if you authored it).
3. `python3 scripts/regenerate-marketplace.py` — the generator's `find_first_party_plugins()` emits it into `plugins[]` with a `./plugins/<name>` source and a `contains:` field listing its bundled skills/agents/commands. Bundled items ride along inside the plugin; they are **not** promoted to the top-level `skills[]`/`agents[]` arrays.
4. `forge list --type plugin | grep <name>` — verify it appears. First-party wins on any name collision with an upstream plugin.

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

`type` is one axis; **`category`** (use-case domain) is the orthogonal second axis — see below.

## Category axis (the use-case domain)

Every marketplace item carries a `category`, one of **9 canonical values**: `engineering`,
`product`, `marketing`, `leadership`, `research`, `finance`, `operations`, `compliance`,
`productivity`. `forge list/search --category <x>` and the TUI `C` key filter on it. Taxonomy
ratified in `docs/PLAN-forge-unification.md` (Appendix A).

`scripts/regenerate-marketplace.py` assigns `category` in one pass (`apply_categories`):
- **First-party** items declare `category:` in their own frontmatter (SKILL.md / agent `.md`) or
  `plugin.json`. Add it when you add the item — a missing one warns and defaults to `productivity`.
- **Upstream** non-plugin items (agents/personas/commands) carry none of their own, so they're
  assigned by name in **`scripts/upstream-category-map.json`** (lives outside `upstream/`, so it
  survives `sync-upstream.sh`). When a `sync-upstream.sh` pull adds new upstream items, add their
  entries to that map or they fall back to `productivity` (the generator warns).
- Raw upstream values are folded to canonical via a collapse map (e.g. `development→engineering`),
  so old categories are normalized automatically.

## Install layer

Managed via [`forge`](https://github.com/flight505/forge) — run `forge guide` for usage. This repo is content + sync only — no CLI of its own.

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
   - If tracking upstream updates matters → prefer `git subtree add` and record provenance in the skill's `_source.yaml`
5. Add a `_source.yaml` with `kind: repo-mirror` (or `subtree` if pulling via git subtree) and the `origin:` URI
6. Run `python3 scripts/regenerate-marketplace.py` and verify it appears in the catalog
7. `forge install <name>` smoke-test from a fresh session

No dedicated skill is needed for this workflow — starting a Claude session with the URL and this CLAUDE.md loaded is sufficient.

## Overlap rules

When `upstream/` and a first-party `skills/` entry share a name, `scripts/regenerate-marketplace.py` defaults to **ours wins** (first-party takes precedence). No exceptions currently exist — `deepwiki` was dropped from `skills/` in favour of upstream's, so there's no live overlap to resolve.

## Conventions

- Python: stdlib only. No pip dependencies in `scripts/`.
- Run `python3 scripts/regenerate-marketplace.py` after any change to `skills/`, `agents/`, `plugins/`, or `upstream/`.
- Commit `marketplace.json` after regeneration.
