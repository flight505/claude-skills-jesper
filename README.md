# claude-skills-jesper

Personal curated marketplace of Claude Code skills, agents, personas, and commands.

**Content sources:**
- `upstream/` — vendored copy of [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) via `git subtree` (268+ skills, 33 agents, 7 personas, 54 commands)
- `skills/` — first-party additions (21-toolkit survivors and anything I author)

**Install layer:** [`forge`](https://github.com/flight505/forge) — registered as a `marketplace-local` source during dev, `marketplace-remote` once pushed.

## Layout

```
.claude-plugin/marketplace.json   ← single merged catalog (generated)
skills/                           ← first-party skills
upstream/                         ← git subtree of alirezarezvani/claude-skills
scripts/
  regenerate-marketplace.py       ← rebuilds marketplace.json from upstream/ + skills/
  sync-upstream.sh                ← git subtree pull --squash + regenerate
  upstream-changelog.py           ← list added/removed/changed since last sync
```

## Workflow

```bash
# Pull latest upstream + regenerate marketplace
./scripts/sync-upstream.sh

# Manually regenerate without pulling
python3 scripts/regenerate-marketplace.py

# Preview what a sync would change
python3 scripts/upstream-changelog.py
```

## Install via forge

```bash
forge source add claude-skills-jesper \
  --kind marketplace-local \
  --path ~/Projects/Dev_projects/Claude_SDK/claude-skills-jesper

forge list --type skill
forge install <name>
```
