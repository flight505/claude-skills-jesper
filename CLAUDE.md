# CLAUDE.md — claude-skills-jesper

Personal Claude Code skills marketplace. Vendors [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) via `git subtree` under `upstream/` and adds first-party skills under `skills/`.

## Critical paths

- `upstream/` — never hand-edit. Pull updates with `./scripts/sync-upstream.sh`.
- `skills/` — first-party only. Edit freely.
- `.claude-plugin/marketplace.json` — **generated**. Never hand-edit; run `python3 scripts/regenerate-marketplace.py`.

## Adding a first-party skill

1. Create `skills/<name>/SKILL.md` with required frontmatter (name, description, version, etc.)
2. `python3 scripts/regenerate-marketplace.py`
3. `forge list --type skill | grep <name>` — verify it appears

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

## Overlap rules

When upstream and first-party have the same skill name:
- **Default: ours wins** (skills/ takes precedence)
- Exceptions tracked in `OVERLAP.md`
- Confirmed exception: `deepwiki` — use upstream's

## Conventions

- Python: stdlib only. No pip dependencies in `scripts/`.
- Run `python3 scripts/regenerate-marketplace.py` after any change to `skills/` or `upstream/`.
- Commit `marketplace.json` after regeneration.
