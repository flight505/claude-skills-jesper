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

Spun out as `chore/stop-tracking-generated-docs` while working through Track 1's secret-scan friction. Two commits, branch pushed (not yet merged):

- [x] Gitignore the 12 auto-regenerated reference files (claude/openrouter/warp doc-skills); cookbook/ stays tracked
- [x] `skills/_shared/install-refresh-daemons.sh` — clone-and-install launchd daemons for all 7 doc-refresh-shaped skills; idempotent; matches existing label convention
- [x] CLAUDE.md documents the entry point
- [x] Smoke-tested locally: 2 new daemons (design-md, gemini-docs) loaded + fired immediately, 5 existing skipped no-op

Followup: open PR + merge https://github.com/flight505/claude-skills-jesper/pull/new/chore/stop-tracking-generated-docs

---

## Track 2 — Item-context chat in `forge tui`

**Goal:** while a catalog item is selected, the user can press a key (proposed: `c`
or `?`) to open a chat pane scoped to that item. Claude answers using the item's
SKILL.md / agent.md / persona.md as context, and can suggest related items from the
catalog. No new dependencies; reuse `aisuggester`'s HTTP + auth layer.

### 2.1 Backend — extend `internal/aisuggester` into a tiny `internal/aichat` package
- [ ] **2.1.1 Carve auth/transport into a shared helper** (`internal/llm/client.go`):
  `resolveAuth()`, `postMessages()`, `readKeychainOAuth()` — currently private in
  `aisuggester`. No behaviour change; aisuggester re-uses it.
- [ ] **2.1.2 New package `internal/aichat`** with `ChatAboutItem(ctx, item, history, userMsg) (reply, tokensUsed, error)`.
  - System prompt template includes: item name, type, description, full body (truncated
    to ~6KB), and a compact list of catalog peers (name + one-liner) so the model can
    suggest pairings.
  - Use `claude-haiku-4-5-20251001` by default (cheap, fast); env override
    `FORGE_CHAT_MODEL`.
  - Cache the system block (`cache_control: ephemeral`) so multi-turn chat in the
    same item pays ~10% of the first turn's input tokens.
- [ ] **2.1.3 Token accounting**: surface input/output tokens per turn so the
  status bar can show a running tally (matches the global "Claude Alerts" rule —
  warn before usage spikes).
- [ ] **2.1.4 Unit tests** with a fake `http.RoundTripper` covering: happy path,
  401 (re-prompt auth), 429 (single retry + backoff), oversized item body (truncate).

### 2.2 TUI — chat pane wired into the catalog screen
- [ ] **2.2.1 New view `ui/views/itemchat.go`** rendered as a right-side or bottom
  pane (decide after mocking — see 2.2.2). Bubble Tea model holds `[]message`,
  `textarea.Model` for input, `viewport.Model` for transcript.
- [ ] **2.2.2 Layout decision**: pick between (a) replacing the preview pane in
  catalog when chat is open, or (b) a full-screen modal. Recommendation: **(a)**
  — keeps the sidebar + list visible so the user can switch items mid-chat and the
  context auto-rebinds.
- [ ] **2.2.3 Key handler in `ui/app.go`**: `c` opens chat for the currently
  selected item; `Esc` closes; switching items in the list resets the transcript
  with a one-line "now chatting about <new item>" notice.
- [ ] **2.2.4 Streaming**: aichat helper returns full response (not streaming) in
  v1 — the spinner already exists. Streaming is a v2 if needed.
- [ ] **2.2.5 Status-bar token counter**: `chat · 1.2k in / 340 out · $0.001` (using
  Haiku 4.5 published rates). Reset on item switch.
- [ ] **2.2.6 No-auth fallback**: if `aisuggester.ErrNoAuth`, show a callout
  pointing at `claude /login` (Claude Max OAuth path) instead of failing.
- [ ] **2.2.7 Tests** in `ui/app_chat_test.go` mirroring the focus-cycle tests:
  open/close, item-switch resets transcript, Enter submits, Esc cancels.

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

## Notes & open questions

- **Cost guardrail.** Each chat turn at Haiku 4.5 rates is ~$0.0005–$0.002. A
  hard ceiling (e.g. `FORGE_CHAT_DAILY_BUDGET_USD`) + warning toast when 80% used
  would respect the "Claude Alerts" global rule. Decide before shipping.
- **Catalog peer list size.** Sending all ~150 items as "peers" in the system
  prompt is ~30KB per first turn. Filtering to same-type + 10 nearest neighbours
  by name keyword keeps it under 5KB. Worth A/B-ing answer quality once the
  pipeline is in place.
- **Streaming on the TUI.** Bubble Tea + SSE is awkward (channels through
  `tea.Cmd`). Skip for v1 unless user feedback says otherwise.
- **Privacy.** All chat traffic goes to api.anthropic.com under the user's own
  credential — same trust boundary as `aisuggester` today. No new disclosure
  needed in README, but mention it in the chat pane's first-launch hint.
