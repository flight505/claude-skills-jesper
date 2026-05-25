# TODO — claude-skills-jesper

> **Status (2026-05-24)**: all 7 tracks shipped. The catalog has an item-context chat in both `forge tui` (press `c` on a row) and `forge serve` (collapsible panel on the Item detail page). `forge suggest --project` (or `p` in the TUI's Suggest view) auto-derives a task from the bound cwd's CLAUDE.md/README/manifests/git log + already-installed list, so you can ask "what's helpful here?" without typing one. Provenance + update-check tooling is in place. Open follow-ups live at the bottom of this file.

## Background

The catalog (~160 items: skills, plugins, agents, personas, orchestrators, commands) mixes first-party content under `skills/` with the vendored `upstream/` from [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills), plus first-party agents under `agents/`. Items now self-declare their provenance via `_source.yaml` manifests (Track 6) and their pairing hints via `pairs_with:` frontmatter (Track 4). The chat panes consume both.

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

## Track 3 — Item-context chat in `forge serve` (web UI) ✅ DONE

Merged in `flight505/forge` (PR #3). Two commits: server endpoint + Solid panel + regenerated SPA bundle. 8 new server tests, 54 total green. Live smoke-tested: POST returned an on-target SKILL.md-grounded reply, ~$0.003.

- [x] **3.1** `POST /api/item/<name>/chat` — non-streaming JSON v1 (matches TUI). SSE deferred; the wire protocol leaves room because the front-end already polls `/api/health` for capability.
- [x] **3.2** `web/src/components/ItemChat.tsx` — collapsible panel inside `Item.tsx`, Cmd/Ctrl+Enter submit, hidden when `health.chat_available` is false
- [x] **3.3** Token tally + USD estimate in the section header (mirrors TUI format); 429 → "rate-limited" callout
- [x] **3.4** `/api/health` exposes `chat_available: bool` via `llm.ResolveAuth`

---

## Track 4 — Catalog enrichment so chat answers are better ✅ DONE

Shipped across two PRs: marketplace side (`claude-skills-jesper#5`) and forge consumer (`flight505/forge#4`). End-to-end: a chat opened on `frontend-learning` now sees `design-md` and `lesson-reviewer` in its peer set ahead of the same-type fill, sourced from `pairs_with:` in frontmatter.

- [x] **4.1** Audit thin descriptions — no remediation needed. All 10 first-party SKILL.md descriptions are ≥130 chars with clear trigger phrases.
- [x] **4.2** `pairs_with:` frontmatter (CSV or YAML-list shape), `regenerate-marketplace.py` parses both, emits as array on the marketplace entry, `Entry.PairsWith` + `Item.PairsWith` in forge schemas, `internal/aichat.SelectPeers` consolidates the TUI + server duplicates and applies pairs-first selection
- [x] **4.3** CLAUDE.md gained a "`pairs_with:` — pairing hints for the chat" section with both syntactic forms + the dangling-name rule
- [x] **4.4** Backfilled 9 items: the design trio (`frontend-learning` ↔ `design-md` ↔ `lesson-reviewer`), the docs trio (`claude-docs` ↔ `openrouter-docs` ↔ `gemini-docs`), the NVIDIA pair (`spark-docs` ↔ `nvidia-dgx-research`), and `perplexity-search` → `claude-docs-skill`. 6 new tests on `internal/aichat.SelectPeers` cover priority ordering, dangling-name drop, dedup, and limit truncation.

---

## Track 5 — Integrate `frontend-learning` as a first-party skill ✅ DONE

Merged as PR #3. Catalog grew from 9→10 skills, 24→25 agents (the first-party `lesson-reviewer` agent at the new top-level `agents/` dir). The standalone source at `~/Projects/Dev_projects/Claude_SDK/frontend-learning/` is gone (`mv` was the deletion). `regenerate-marketplace.py` learned to walk `./agents/` for first-party agents in addition to `upstream/agents/`.

- [x] **5.1** Cleanup (demo lesson, _test dir, .DS_Store, standalone marketplace.json, plugins/ wrapper)
- [x] **5.2** Shape decided: `skills/frontend-learning/` for skill content, repo-root `agents/` for first-party agents (mirrors the `skills/` pattern)
- [x] **5.3** Move complete; `lesson-base.css` left at top level (SKILL.md path references stayed correct)
- [x] **5.4** Marketplace regenerator extended (+10 lines) + first-party agents discovery + `OVERLAP.md` merge for collisions
- [x] **5.5** End-to-end install verified: `forge install frontend-learning` populated `~/.claude/skills/frontend-learning/`, Claude Code's skill loader picked it up immediately; agent lands at `~/.claude/agents/lesson-reviewer.md` and becomes discoverable on next session restart
- [x] **5.6** Source dir deletion verified; no launchd plists referenced the old path

Side benefit picked up during Track 4: `frontend-learning ↔ design-md ↔ lesson-reviewer` got declared as a `pairs_with:` triangle, so chats opened on any of them surface the others as suggested pairings.

---

## Track 6 — Sources taxonomy + unified update check ✅ DONE

Merged as PR #4 + follow-up bug-fix (`3c6f9e3`, `launchctl kickstart gui/$UID/<label>` needed to be one arg). Eleven manifests + a stdlib-only aggregator. The directory restructure (6.4.2) was deferred per the recommendation — metadata captured provenance without breaking the install layer.

- [x] **6.1** Manifest schema (`kind`, `origin`, `version`, `refresh.{method,script,schedule}`, `notes`) documented in CLAUDE.md
- [x] **6.2** Backfilled 11 manifests: 4 originals (`apple`, `frontend-learning`, `perplexity-search`, `agents/`), 6 docs (claude/openrouter/warp/gemini/spark/nvidia-dgx-research), 1 repo-mirror (`design-md` ← `npm:getdesign`). Reclassified `nvidia-dgx-research` from "original" to "docs" — it does fetch a llms.txt catalog on cron.
- [x] **6.3** `scripts/check-sources.py` — walks every manifest, probes per-kind (mtime for docs, npm registry for repo-mirror, `git log` against the subtree squash for upstream). `--fix` runs the right refresh action (launchctl kickstart for docs, update script for repo-mirror, sync-upstream.sh for subtree).

### Side finding surfaced + cleared
The first dry-run flagged 5 doc-skills with empty `references/` on disk. `--fix` fired the daemons; all populated within a few minutes. The launchctl bug-fix above was discovered + landed in the same session.

### Deferred
- **6.4.1** Forge UI surface for check-sources output (Doctor section). Open follow-up — not blocking.
- **6.4.2** Directory restructure. Not pursued; the manifest captures provenance, the structural change would break the install layer. Revisit only if metadata proves insufficient.

---

## Architecture-review cleanup (2026-05-25) ✅ DONE

cs-senior-engineer architecture review of the forge codebase produced a punch list of 1 high-severity bug + 11 medium/low items. Authored two durable agents (`surgical-fix-builder` + `surgical-fix-validator`) for this kind of work, then worked the list across 4 PRs in forge:

- **PR #6** — gofmt sweep, `Catalog.Load` error-swallow bug + 4 regression tests, server + UI context plumbing, `ItemType.Short()` callers, version-constant consolidation, CI `gofmt -l` gate
- **PR #7** — sources view async refresh, aisuggester struct hoist, `suggest --project` dedup, sort.Slice
- **PR #8** — `ui/app.go:Update` 254-line method split into 4 per-mode handlers (`updateConfirmInstallKeys`, `updateOverlayKeys`, `updateSidebarKeys`, `updateGlobalKeys`); 10 focus tests stay green
- **PR #9** — table-driven tests for `internal/{installer,surfaces,sources}` (24 new tests; was zero)
- **PR #10** — delete `pkg/api` stub (40 lines, zero callers, illusion-of-stable-API)

Test count: 58 → 82. CI lint gate exercises gofmt + vet on every PR.

## Open follow-ups (2026-05-25 pass — 3 of 4 closed)

**Closed:**

- ✅ **Forge UI surface for `check-sources`** — `forge tui` → F6 (Doctor) → press `s`. Runs `scripts/check-sources.py --no-color` async, renders inline with amber STALE lines. forge PR #11.
- ✅ **Document the third-party integration workflow** — 7-step "Integrating a third-party repo" section added to CLAUDE.md.
- ✅ **DGX Spark / Linux portability review** — `docs/linux-install.md` added. Short answer: forge binary is already cross-platform; only the launchd daemon installer needs a cron/systemd equivalent. Guide covers build-from-source, env-var auth, cron + systemd timer setups, headless URL-open note. `platform/open.go` already handles `xdg-open`; `llm/client.go` already darwin-gates the Keychain probe.

**Still open (conditional):**

- **Streaming on the TUI.** Deliberate non-implementation: Haiku 4.5 responds in 2-5 seconds; "thinking…" indicator is visible; web is also non-streaming and feels fine. Implement only if multi-paragraph replies become a real UX complaint in practice. The Bubble Tea chain-cmd pattern (each chunk emits a new Cmd) is documented in the codebase as a comment; the Anthropic streaming API path in `internal/llm` would need a parallel `Stream()` function alongside `Post()`.

---

## Track 7 — Project-aware `suggest` ✅ DONE

Merged in `flight505/forge` (PR #5, commit `1361d29`). From a `! forge` invocation inside a Claude Code session — or just `forge suggest --project` from anywhere with a CLAUDE.md/README — forge now reads project context and ranks catalog items against it. No task description needed.

- [x] **7.1** `internal/project/profile.go` — reads CLAUDE.md, README, package.json/pyproject/Cargo/go.mod, `git log -20`, already-installed list. 10 KB cap with per-source budget. Stdlib only.
- [x] **7.2** `forge suggest --project` + `forge agent suggest --project` — task arg optional when `--project` set; implies `--smart`; JSON envelope gains `project_signals: [...]`
- [x] **7.3** TUI Suggest view: `p` auto-fills textarea + enters edit mode (no auto-submit, user previews/tweaks)
- [x] **7.4** `(installed)` annotation on CLI output, `installed: bool` per suggestion in JSON
- [x] **7.5** 8 tests in `internal/project/profile_test.go` cover empty dir, file collection, candidate priority, mid-source truncation, already-installed signal, git-log gating, whitespace skip, Cwd defaulting
- [x] **7.6** Smoke-tested from two project roots — `claude-skills-jesper` produced suggestions citing `regenerate-marketplace.py` + `sync-upstream.sh`; `forge` produced HTTP-server + Go-state-machine suggestions. Same command, different cwd, contextually distinct results.

### Decisions made during implementation

- **Task assembly**: shipped option A (factual concatenation). No Haiku pre-summarisation step. Quality felt good in smoke tests; upgrade later if needed.
- **`.gitignore` handling**: skipped. v1 only reads explicitly-named root files which aren't typically gitignored. Add `git ls-files` later if we ever do a recursive walk.
- **Recursive walk**: not implemented. Root-level files only. v2 could pick up `docs/*.md` if it proves useful.
- **Auto-submit**: not added. TUI `p` always enters edit mode so the user sees what's being asked. The CLI runs immediately because the user typed a flag; that's its own form of consent.
- **Web parity**: deferred. Earn it after CLI/TUI versions see use.
