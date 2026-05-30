# claude-skills-jesper

Personal curated marketplace of Claude Code skills, plugins, agents, personas, and commands.

**Content sources:**
- `upstream/` — vendored copy of [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) via `git subtree`. The bulk of the catalog: 64 plugins, 24 agents, 7 personas, 38 commands.
- `skills/` + `agents/` — first-party items I author and maintain (10 skills, 3 agents).

Merged catalog total: **146 items** (10 skills · 64 plugins · 27 agents · 7 personas · 38 commands), generated into `.claude-plugin/marketplace.json`.

**Install layer:** [`forge`](https://github.com/flight505/forge) — run `forge guide` to learn how to use it.

## Layout

```
.claude-plugin/marketplace.json   ← single merged catalog (generated — never hand-edit)
skills/                           ← first-party skills
agents/                           ← first-party agents
upstream/                         ← git subtree of alirezarezvani/claude-skills (never hand-edit)
scripts/
  regenerate-marketplace.py       ← rebuilds marketplace.json from upstream/ + skills/ + agents/
  sync-upstream.sh                ← git subtree pull --squash + regenerate
  upstream-changelog.py           ← list added/removed/changed since last sync
  check-sources.py                ← report first-party items with upstream updates available
```

## Workflow

```bash
# Pull latest upstream + regenerate the marketplace
./scripts/sync-upstream.sh

# Regenerate without pulling (after editing skills/ or agents/)
python3 scripts/regenerate-marketplace.py

# Preview what a sync would change
python3 scripts/upstream-changelog.py
```

## Install via forge

```bash
# Register this repo as a forge source (kind defaults to marketplace-local)
forge source add claude-skills-jesper --path ~/Projects/Dev_projects/Claude_SDK/claude-skills-jesper

forge guide            # how to use forge
forge list             # browse the catalog
forge install <name>   # install into a surface (defaults to claude-cli-user)
```

See [CLAUDE.md](CLAUDE.md) for maintenance details — adding first-party skills, `_source.yaml` provenance manifests, and the doc-skill refresh daemons.
