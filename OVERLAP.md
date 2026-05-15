# Overlap decisions

When `upstream/` and `skills/` contain a skill with the same name, the resolver in `scripts/regenerate-marketplace.py` defaults to **ours wins** (skills/).

Override with explicit entries below. Format: `name | winner | reason`.

| name      | winner   | reason                                                                 |
|-----------|----------|------------------------------------------------------------------------|
| deepwiki  | upstream | alirezarezvani's version is more current and better integrated         |

Skills dropped from the 21-toolkit migration (not included in `skills/`):

- `deepwiki` — using upstream's
- `project-bootstrapper` — unused
- `hooks-mastery` — unused
- `skill-manager` — old claude-toolkit relic
