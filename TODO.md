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

## Track 1 — Upstream catalog refresh

Confirmed: `scripts/sync-upstream.sh` works. Remote `upstream-skills` is configured
and `git subtree pull --squash` is the merge mechanism. Last sync was at upstream
`0970924` / commit `4a33dc7` (Oct ~2025). **979 upstream commits pending.**

- [ ] **1.1 Dry-run the upstream changelog** to see what would land:
  `python3 scripts/upstream-changelog.py --against upstream-skills/main | tee /tmp/upstream-preview.md`
- [ ] **1.2 Review for breaking changes** (renamed dirs, schema shifts) before merging — the
  diff is large; expect collisions with `OVERLAP.md` entries.
- [ ] **1.3 Sync** on a feature branch: `git switch -c chore/upstream-sync-2026-05 && ./scripts/sync-upstream.sh`
- [ ] **1.4 Re-run `regenerate-marketplace.py --verbose`** and diff `marketplace.json` —
  expect new plugins, agents, personas to appear; verify slug stability.
- [ ] **1.5 Smoke-test in forge**: `forge tui` → catalog count should rise; spot-check 3
  new items each for skill/plugin/agent/persona.
- [ ] **1.6 Update `OVERLAP.md`** with any new collisions discovered (default: ours wins).

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
