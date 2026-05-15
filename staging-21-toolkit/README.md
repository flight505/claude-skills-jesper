# Staged 21-toolkit content

These directories are the 21-toolkit skills migrated from `skill-forge/skills/21-toolkit/` before that repo was retired. They are **not yet** included in `marketplace.json`.

**Original source:** `~/Projects/Dev_projects/Claude_SDK/claude-toolkit/skills/` → migrated into `skill-forge/skills/21-toolkit/` → staged here.

## To do (separate session)

Review each directory and decide:
- **Promote** to first-party — move to `../skills/<name>/` (will be picked up by `regenerate-marketplace.py`)
- **Drop** — already-decided drops: `deepwiki` (using upstream's), `project-bootstrapper`, `hooks-mastery`, `skill-manager`
- **Defer** — leave staged until a real use surfaces

## Inventory

| Directory                       | Decision                          |
|---------------------------------|-----------------------------------|
| `_shared/`                      | TBD — looks like helper assets    |
| `ai-startup-advisor/`           | TBD                               |
| `app-onboarding-questionnaire/` | TBD                               |
| `apple/`                        | TBD — deeply nested, big          |
| `applescript/`                  | TBD                               |
| `claude-docs-skill/`            | LIKELY KEEP — referenced in global CLAUDE.md |
| `deepwiki/`                     | DROP — use upstream's             |
| `design-md/`                    | TBD                               |
| `fusion360-scripting/`          | TBD                               |
| `gemini-docs-skill/`            | LIKELY KEEP — global CLAUDE.md ref |
| `hooks-mastery/`                | DROP — unused                     |
| `install-and-maintain/`         | TBD — old-toolkit infra?          |
| `install-toolkit-skills/`       | TBD — old-toolkit infra?          |
| `marketplace-manager/`          | TBD — superseded by forge?        |
| `openrouter-docs-skill/`        | LIKELY KEEP — global CLAUDE.md ref |
| `perplexity-search/`            | TBD                               |
| `project-bootstrapper/`         | DROP — unused                     |
| `skill-manager/`                | DROP — old claude-toolkit relic   |
| `version-manager/`              | TBD                               |
| `warp-docs-skill/`              | LIKELY KEEP — global CLAUDE.md ref |
| `webapp-testing/`               | TBD                               |

When promoting:
```bash
mv staging-21-toolkit/<name> skills/<name>
python3 scripts/regenerate-marketplace.py
```
