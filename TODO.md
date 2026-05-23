# TODO — claude-skills-jesper

## Background

The catalog (~150 items: skills, plugins, agents, personas, orchestrators, commands)
mixes first-party content under `skills/` with the vendored `upstream/` from
[alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills).
Many upstream items have terse one-liners or no usage hints, so users open `forge`
and can't tell:
- what the item actually does in practice
- which surface(s) it makes sense on
- which other items it pairs with (e.g. a persona + an orchestrator + a skill)

`forge` already has `internal/aisuggester/aisuggester.go` calling the Messages API
(via Claude Code OAuth / Keychain / `ANTHROPIC_API_KEY`) for the **suggest** command.
The next step is to reuse that auth + transport for an **item-context chat** so the
user can ask "what does this do?" / "what should I pair it with?" right inside
`forge tui` and `forge serve`.

---

## Track 1 — Upstream catalog refresh ✅ DONE

Synced 2026-05-23 on branch `chore/upstream-sync-2026-05` (merged to main).
Catalog delta: 44→61 plugins, 20→24 agents, 33→38 commands. Zero removals.

- [x] **1.1 Dry-run the upstream changelog**
- [x] **1.2 Review for breaking changes** — bundle→individual refactors only, no destructive renames
- [x] **1.3 Sync** on feature branch + subtree pull
- [x] **1.4 Re-run `regenerate-marketplace.py --verbose`** + diff marketplace.json
- [x] **1.5 Smoke-test** — spot-checked syllabus, compliance-os, cs-frontend-engineer, handoff
- [x] **1.6 OVERLAP.md** — no new collisions vs first-party (verified by name-set diff)

---

## Track 1b — Stop tracking auto-generated doc refs ✅ DONE

Merged as PR #2. Three commits total (gitignore + untrack, daemon installer, extended gitignore to 4 more doc-skills).

- [x] Gitignore all auto-regenerated reference files across 7 doc-skills; cookbook/ stays tracked
- [x] `skills/_shared/install-refresh-daemons.sh` — clone-and-install launchd daemons; idempotent; matches existing label convention
- [x] CLAUDE.md documents the entry point
- [x] PR opened + merged

---

## Track 2 — Item-context chat in `forge tui` ✅ DONE

Merged in `flight505/forge`. Three commits: llm extraction, aichat backend + tests, TUI wiring + tests. 17 new tests, all 38 pass. `c` on a catalog row opens a chat pane scoped to that item; Ctrl+S sends, Esc closes; statusbar shows a running token tally with rough USD estimate.

### 2.1 Backend
- [x] **2.1.1** Carved auth + transport into `internal/llm` (zero-behavior refactor)
- [x] **2.1.2** New `internal/aichat.ChatAboutItem` with cache-controlled system block, Haiku 4.5 default, `FORGE_CHAT_MODEL` override, 6KB rune-safe body truncation
- [x] **2.1.3** Token accounting (4-field Usage struct returned per turn)
- [x] **2.1.4** Unit tests with fake `http.RoundTripper`: env precedence, OAuth vs api-key headers, 401/429 surfacing, body forwarding, system prompt shape, FORGE_CHAT_MODEL override, ephemeral cache_control, usage parsing

### 2.2 TUI
- [x] **2.2.1** `ui/views/itemchat.go` — Bubble Tea textarea + viewport + transcript
- [x] **2.2.2** Picked option (a): replaces preview pane when chat is active
- [x] **2.2.3** `c` opens, `Esc` closes (item-switch-while-chat deferred — Esc → navigate → c re-opens; works fine for v1)
- [x] **2.2.4** No streaming (deferred to v2; spinner suffices)
- [x] **2.2.5** Statusbar token tally with USD estimate
- [x] **2.2.6** `ErrNoAuth` → "[chat needs auth]" callout in transcript
- [x] **2.2.7** Tests: opening notice, reply/error handling, ErrNoAuth → noAuth flag, Esc/Ctrl+C pass-through, SwitchItem reset semantics, TokenSummary states, SelectPeers same-type/limit

---

## Track 3 — Item-context chat in `forge serve` (web UI)

Parity goal: same chat capability on the SPA. Reuses the new `internal/aichat`
backend; web only adds a route + a UI panel.

- [ ] **3.1 HTTP route** `POST /api/item/:name/chat` with body
  `{ history: Message[], message: string, type?: string }` → SSE or JSON
  response. **Recommendation: SSE** — the web client benefits from streaming
  visibly more than the TUI does.
- [ ] **3.2 Solid component `web/src/components/ItemChat.tsx`** rendered inside
  the Item detail screen, collapsible (default collapsed so the existing layout
  isn't disrupted).
- [ ] **3.3 Token-usage badge** mirroring the TUI status bar; rate-limit guidance
  if 429.
- [ ] **3.4 Health probe** in `/api/health` should expose `chat_available: bool`
  so the UI can hide the panel cleanly when no credential is configured.

---

## Track 4 — Catalog enrichment so chat answers are better

Even with chat, vague item descriptions degrade the model's answers. These are
content-side fixes inside `claude-skills-jesper`, not code in `forge`.

- [ ] **4.1 Audit first-party `skills/` for thin descriptions** (one-liner only,
  no usage example): list them with `python3 scripts/regenerate-marketplace.py
  --verbose 2>&1 | grep -i 'no description'` — then expand each.
- [ ] **4.2 Add a `pairs_with:` frontmatter field** (optional) to SKILL.md /
  agent / persona files. Update `regenerate-marketplace.py` to surface it in
  `marketplace.json`. The chat system prompt (Track 2.1.2) reads this and uses
  it for pairing suggestions instead of guessing.
- [ ] **4.3 Document the convention** in `CLAUDE.md` under "Adding a first-party
  skill" — short paragraph + example block.
- [ ] **4.4 Backfill pairing hints** for the most-used items first (top 10 by
  install frequency once `forge serve` exposes that metric, otherwise pick
  manually: handoff, code-reviewer, frontend-design, etc).

---

## Track 5 — Integrate `frontend-learning` as a first-party skill

`/Users/jesper/Projects/Dev_projects/Claude_SDK/frontend-learning/` (not a git repo) is a standalone Claude Code plugin that generates single-file HTML explainers in the spirit of 3Blue1Brown/Distill/Ciechanowski. ~150KB total: 1 SKILL.md, 1 agent (`lesson-reviewer`), 5 shell/python scripts, 4 reference docs (html-template, interactive-patterns, pedagogy-principles, STYLE_PRESETS, lesson-qa-checklist), 1 CSS file. The standalone `plugins/` wrapper exists because of a one-off Claude Desktop install path — dropping it for now.

Goal: land it under `skills/frontend-learning/` so `regenerate-marketplace.py` picks it up and `forge install frontend-learning` works.

### 5.1 Cleanup in the source directory (before move)
- [ ] **5.1.1** `trash lessons/2026-05-21-attention-in-transformers.html lessons/2026-05-21-attention-in-transformers.meta.json` — demo lesson, generated output
- [ ] **5.1.2** `trash lessons/_test/` — hash-function test artifacts
- [ ] **5.1.3** `find . -name .DS_Store -delete`
- [ ] **5.1.4** `trash .claude-plugin/marketplace.json` — standalone marketplace shape, superseded by parent
- [ ] **5.1.5** `trash plugins/` — Claude Desktop wrapper, no longer needed

### 5.2 Decide shape under `skills/frontend-learning/`
- [ ] **5.2.1** Read `scripts/regenerate-marketplace.py` to confirm what first-party agents look like (current first-party agents: check if there are any examples; if not, this is the first one). Decide whether the agent lives at `skills/frontend-learning/agents/lesson-reviewer.md` (likely) or top-level `skills/agents/`.
- [ ] **5.2.2** Confirm scripts/ subdir is supported. Likely yes — claude-docs-skill, design-md, etc. all have scripts/.
- [ ] **5.2.3** Confirm a top-level `lesson-base.css` is OK as a reference asset (not in `references/`). Either move to `references/lesson-base.css` to match the convention, or leave at top level and update SKILL.md path references.

### 5.3 Move
- [ ] **5.3.1** `mv /Users/jesper/Projects/Dev_projects/Claude_SDK/frontend-learning skills/frontend-learning` (post-cleanup)
- [ ] **5.3.2** Adjust SKILL.md internal paths if 5.2.3 reorganized anything
- [ ] **5.3.3** Verify `.gitignore` patterns still make sense — the standalone gitignore had `lessons/*.html`, `lessons/*.meta.json`; either fold those into the top-level `.gitignore` or keep a skills-local `.gitignore`

### 5.4 Wire into marketplace
- [ ] **5.4.1** `python3 scripts/regenerate-marketplace.py --verbose` — verify frontend-learning appears under `skills:` (or `plugins:` if treated that way)
- [ ] **5.4.2** Verify the agent `lesson-reviewer` appears under `agents:`
- [ ] **5.4.3** Commit + push

### 5.5 Verify forge installs cleanly
- [ ] **5.5.1** `forge agent search frontend-learning` — should return at least one match
- [ ] **5.5.2** `forge install frontend-learning --surface claude-cli-user --method link` — verify symlink lands, scripts are executable, SKILL.md frontmatter parses
- [ ] **5.5.3** Trigger the skill from a Claude Code session (e.g. "teach me X") — confirm Claude picks it up

### 5.6 Delete the source
- [ ] **5.6.1** Only after 5.5 passes: `trash /Users/jesper/Projects/Dev_projects/Claude_SDK/frontend-learning` (the now-empty original location)
- [ ] **5.6.2** Check the macOS launchd daemons — does anything reference the old path? (Should be none; frontend-learning doesn't have an update script.)
- [ ] **5.6.3** Update any external docs/notes that pointed at the old path (the user's CLAUDE.md if it does, mental model, etc.)

### Notes
- All work happens on a feature branch (`feat/integrate-frontend-learning`), not main.
- The new skill becomes a candidate for Track 4.2 `pairs_with:` enrichment — natural pair with `frontend-design` and `design-md`.

---

## Track 6 — Sources taxonomy + unified update check

Today the `skills/` directory mixes four different provenance kinds, all visually equal:

| Kind | Examples | Refresh mechanism today |
|---|---|---|
| **Original** (mine, hand-edited) | `apple`, `frontend-learning`, `perplexity-search`, `nvidia-dgx-research` | None — manual edits |
| **Docs** (mine, scraped from upstream sites) | `claude-docs-skill`, `openrouter-docs-skill`, `warp-docs-skill`, `gemini-docs-skill`, `spark-docs-skill` | Launchd weekly via `install-refresh-daemons.sh` (Track 1b) |
| **Repo-mirror** (third-party origin, vendored snapshot) | `design-md` (from `getdesign` npm) | Launchd weekly via the same daemon — but conceptually distinct |
| **Subtree** (third-party marketplace, vendored) | `upstream/` (alirezarezvani/claude-skills) | Manual: `./scripts/sync-upstream.sh` |

Three problems this causes:
- No single command answers "what updates are available across all my sources?"
- Adding a new repo-mirror skill (e.g. some github-hosted set of agents) has no documented pattern
- A reader of the repo can't tell from `skills/<name>/` whether a directory is mine-original, mine-docs, or mirrored

**Recommendation: metadata over restructure.** Keep the current directory layout (avoids breaking forge paths, launchd plists, ~/.claude/ symlinks, and ~14 entries in marketplace.json) and add a per-item `_source.yaml` declaring provenance + refresh method. Then build one aggregator script that reads every manifest, runs the right "check for updates" probe per kind, and prints a punch list.

### 6.1 Define the manifest schema
- [ ] **6.1.1** Decide schema. Strawman:
  ```yaml
  # skills/<name>/_source.yaml
  kind: original | docs | repo-mirror | subtree
  origin: ""                # empty for original; URL/npm-pkg/etc for others
  refresh:
    method: none | launchd | manual | subtree
    script: scripts/update-*.sh   # optional, when relevant
    schedule: weekly-sunday-0400  # for launchd kind
  notes: ""                 # one-liner explaining why this skill is here
  ```
- [ ] **6.1.2** Document the schema in `CLAUDE.md` (one paragraph + the example).
- [ ] **6.1.3** Add a top-level `agents/_source.yaml` too — first-party agents are conceptually originals.

### 6.2 Backfill manifests for the current catalog
- [ ] **6.2.1** `original`: apple, frontend-learning, perplexity-search, nvidia-dgx-research
- [ ] **6.2.2** `docs`: claude-docs-skill, openrouter-docs-skill, warp-docs-skill, gemini-docs-skill, spark-docs-skill (origin = the live docs URL the update script scrapes)
- [ ] **6.2.3** `repo-mirror`: design-md (origin = `npm:getdesign`)
- [ ] **6.2.4** `subtree`: skip — `upstream/` itself stays manifest-less because its metadata lives in `.git/refs/upstream-skills` + the squash commit subject.

### 6.3 Build `scripts/check-sources.py` (stdlib only)
- [ ] **6.3.1** Walk every `skills/*/_source.yaml` and `agents/_source.yaml`. Group by kind.
- [ ] **6.3.2** For each kind, probe "what's newer than what we have?":
  - `original`: no-op (skip)
  - `docs`: check the last-modified timestamp of `references/` files vs `.last-fetch` sentinel; "stale if older than N days"
  - `repo-mirror`: query the origin (npm registry for `getdesign`, etc.) and compare against a `version:` field in the manifest
  - `subtree`: shell out to `git fetch upstream-skills main` + `git log <last-squash>..upstream-skills/main` count
- [ ] **6.3.3** Output as a punch list:
  ```
  [docs]
    claude-docs-skill        last fetched 3 days ago — fresh
    openrouter-docs-skill    last fetched 8 days ago — STALE (run scripts/update-*.sh or wait for Sunday)
  [repo-mirror]
    design-md                local 0.6.20 → npm latest 0.6.21 — UPDATE AVAILABLE
  [subtree]
    upstream                 12 new commits since last sync — review with scripts/upstream-changelog.py
  ```
- [ ] **6.3.4** Add `--fix` mode that runs the appropriate refresh action per item (`launchctl kickstart` for docs, `update-templates.sh` for design-md, `sync-upstream.sh` for subtree). Default is read-only.

### 6.4 Optional follow-ups (defer unless useful)
- [ ] **6.4.1** Forge UI: expose the check-sources output in a new Doctor section or as a TUI overlay.
- [ ] **6.4.2** Directory restructure (`docs/`, `mirrors/`, `originals/`). Only if 6.1-6.3 prove insufficient. Cost is high: rebake 7 launchd plists, re-point ~5 symlinks under `~/.claude/skills/`, update `regenerate-marketplace.py`, every marketplace.json path, every doc-skill `.gitignore` rule, every existing forge install anywhere. Benefit is mostly cosmetic given the manifest already exposes provenance.

### Why this order
6.1-6.3 are non-breaking — the existing layout keeps working. Once those land, you have the unified-update-check you wanted AND each item self-declares its provenance, so the directory restructure (6.4.2) becomes a pure cosmetic call rather than a mixed cosmetic + functional one.

---

## Notes & open questions

- **Cost guardrail.** Track 2 shipped without a hard daily budget — running tally is visible in the statusbar but nothing stops a runaway loop. Worth revisiting if usage gets noisy: `FORGE_CHAT_DAILY_BUDGET_USD` env + a warning toast at 80% would respect the global "Claude Alerts" rule.
- **Catalog peer list size.** Currently uses `SelectPeers` (same-type, take first 10 — no relevance ranking). Each first turn sends ~2–3KB of peer summaries. Worth A/B-ing ranking strategies once chat sees real use (semantic via aisuggester? frecency? `pairs_with:` from Track 4.2?).
- **Streaming on the TUI.** Bubble Tea + SSE is awkward (channels through `tea.Cmd`). Skipped for v1. Reconsider if multi-paragraph replies feel sluggish.
- **Privacy.** All chat traffic goes to api.anthropic.com under the user's own credential — same trust boundary as `aisuggester` today. Mention in chat pane's first-launch hint when we add one.
