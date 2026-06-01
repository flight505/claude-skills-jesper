# TODO — locked architecture decisions

> The original TODO tracked 7 shipped implementation tracks (all merged; in git history).
> It was then replaced by four **open** architectural questions (A1–A4). As of **2026-06-01**
> those questions are **decided** — researched (krew/Homebrew/asdf/Helm precedent + the forge
> codebase) and locked below. What remains is **execution**, not deliberation.

**Framing fact that settled everything:** `forge` is a **personal tool** — it runs on Jesper's
machines (MacBook, ml-server, DGX Spark). It is *not* a general/community tool. (If a 2–4 person
team ever shares it, forge gets modified first — a separate future event.) That single fact flips
the repo-structure decision from "two repos like krew" to "one repo," because the only reason to
split a tool from its content is to insulate a *general* tool's release/issue cycle from a
third-party content-PR firehose — which a personal, vendored, generated catalog doesn't have.

The two halves in play today:
- **forge** (`flight505/forge`) — the Go CLI/TUI installer. Organizes by **type**: skill · plugin
  · agent · persona · command.
- **this repo** (`claude-skills-jesper`) — the content. `upstream/` (vendored
  `alirezarezvani/claude-skills` via `git subtree`) + a thin first-party layer (`skills/`,
  `agents/`, `plugins/`), merged into `.claude-plugin/marketplace.json` by
  `scripts/regenerate-marketplace.py`.

---

## Glossary (D4 — canonical; mirror byte-identical into forge's README + CLAUDE.md)

One word per concept. Code and docs currently drift; pin these.

| concept | canonical term | notes / what to stop saying |
|---|---|---|
| the `.forge.json` file | **loadout** | struct is `Loadout`, README title is "Loadouts". "manifest" is overloaded ecosystem-wide → demote to a generic gloss only. Fix `init.go:79` help text ("manifest" → "loadout"). |
| a thing in the catalog | **item** | never "add-on"; **entry** = the `marketplace.json` *shape* only (`schemas.Entry`, internal). |
| a registered provider | **source** | the marketplace is forge's *default source*. |
| merged view of all sources | **catalog** | `internal/catalog/catalog.go` `Catalog` type. ← this is why the rename below is **not** `forge-catalog`. |
| the on-disk source repo/file | **marketplace** (`marketplace.json`) | fine as the artifact noun; not the in-memory concept. |
| install target | **surface** | already consistent everywhere; keep. |
| what a thing **is** | **type** | skill / plugin / agent / persona / command. One axis. |
| what a thing is **for** | **category** | the machine field (`schemas.Item.Category`) + the existing `--category` flag. "domain" / "use-case field" = informal gloss only — don't let prose drift to a second word. |

---

## W1 — Publish the glossary (was A1)  ·  small

Drop the table above as a `## Glossary` block, byte-identical, into forge's README and CLAUDE.md
(and surface the key terms in `forge guide`). Also fix `init.go:79` ("manifest" → "loadout") so
code help matches. Lands naturally inside the monorepo (W4); until then, keep them in sync by hand.

---

## W2 — Source rename behind an alias (was A2)  ·  forge change, then a 1-line rename

**Decided name: `forge-market`** (not `forge-catalog` — that collides with the `Catalog` type =
the merged-view concept). Matches the `marketplace.json` artifact; survives the monorepo merge
unchanged (it's just the source id either way).

**Mechanism: per-source `aliases: []`** — the Homebrew `formula_renames.json` pattern, the *only*
family that keeps **already-committed downstream `.forge.json`** working with **zero edits**
(npm/cargo consumer-side aliases can't — they'd require editing the very files we're protecting).

Forge change (small, well-scoped):
- Add `Aliases []string` to `RegistryEntry` (`internal/catalog/registry.go:13`).
- Check aliases in `resolveSourcePath` (`internal/installer/installer.go:159`) **and**
  `resolveMarketplaceRoot` (`installer.go:181`): if `items[].source` matches no source `id`, scan
  `aliases[]`.

**Migration order — never breaks at any step:**
1. Ship the alias resolver. Release. *(Resolver must precede the rename.)*
2. Rename the source id → `forge-market`, add `"aliases": ["claude-skills-jesper"]` in the same
   change. Update the default-source registry (`registry.go`) + `~/.forge/sources.json`.
3. Downstream `.forge.json` with `source: "claude-skills-jesper"` keep working via the alias —
   **no edits required** (sparkpad ×4, etc.). Keep the alias entry forever (cost ≈ nothing).
4. *(Optional, later)* opt-in `forge migrate` to rewrite old ids — **never** silent rewriting.

**`URL:` field is low-risk** — GitHub's repo-rename redirect keeps old `git clone` URLs working
indefinitely. Still update it explicitly; just don't let the old repo name get re-squatted.

Remaining hardcoded sites to flip at step 2: `registry.go` ×6 (the `ID`, 2 dev-path probes, the
`URL`), `internal/surfaces/cowork_test.go`, `~/.forge/sources.json`, `~/.claude/settings.json`.

---

## W3 — Category as a first-class axis (was A4)  ·  smaller than it looked

**Correction:** `forge list --category` **already exists** (`internal/cli/list.go:18,51,67`) and
`schemas.Item.Category` is populated from `marketplace.json`. So the axis is half-built. Remaining:

1. **Backfill the data.** Today `category` is on 63/65 plugins, **0** of 27 agents / 38 commands /
   7 personas / 10 skills, + 2 plugins, + all first-party.
   - First-party: add `category:` to frontmatter (`regenerate-marketplace.py` already reads it).
   - Upstream non-plugins: derive from a **committed domain-map in *this* repo** (never edit
     `upstream/`); `regenerate-marketplace.py` applies it. The map must **survive
     `sync-upstream.sh`**.
2. **Extend the axis** to where it's missing: add `--category` to `search`
   (`internal/cli/search.go` — one `StringVar` + a filter mirroring `--type`) and a category
   grouping/filter in the TUI (`ui/views/catalog.go` has `typeFilter` but no `categoryFilter`).
3. **Normalize the vocabulary.** The 15 raw values (`development` 26, `leadership` 8, `research` 8,
   `productivity` 5, `product` 4, `marketing` 3, + 9 singletons: `compliance`, `project-management`,
   `business-growth`, `finance`, `design`, `knowledge`, `operations`, `commercial`, `research-ops`)
   are over-fragmented. Pick a canonical ~8–10 set and map both the raw values and the README's
   prose domains into it. Don't break the type-based install dirs.

---

## W4 — Merge into one repo, vertical separation (was A3)  ·  the big one — needs a migration plan

**Decided: one repo.** Separation has caused repeated real issues (drift, the "agents forget the
two halves are connected" confusion, the hardcoded-but-undocumented default URL). Merging removes
the failure mode *by construction* rather than papering over it with cross-doc links. `git subtree`
is designed to embed third-party history inside a monorepo, so the `upstream/` vendoring survives.

Vertical separation inside the merged tree (illustrative — settle in the migration plan):
```
forge/                  # repo root = the tool's name
  cmd/ internal/ ui/    # the Go CLI/TUI
  catalog/              # was claude-skills-jesper
    upstream/           #   vendored subtree (unchanged)
    skills/ agents/ plugins/   # first-party
    scripts/            #   regenerate-marketplace.py, sync-upstream.sh, ...
    .claude-plugin/marketplace.json
  CLAUDE.md README.md   # one each — subsume the glossary (W1) + old cross-link goal
```

**This is a migration, not an edit — write a short plan before executing.** Open questions for the
plan (the *how*; the *whether* is decided): which repo's history is the base vs. subtree-merged;
where forge's default-source path points post-merge (in-repo path vs. still a named source);
CI/release (tool binary vs. catalog regeneration in one tree); does the source id stay `forge-market`
or become a local/default source. W2's alias guarantees downstream `.forge.json` survive the move
regardless.

---

## Sequence

1. **W1 glossary** — cheap, unblocks shared vocabulary. *(do now)*
2. **W2 alias resolver** (forge code) — prerequisite for any safe rename; independent of the rest.
   The actual id rename can land any time after, non-breaking.
3. **W3 category** — mostly data + a small `search`/TUI patch.
4. **W4 monorepo merge** — last and deliberate; subsumes the rename's repo half and the old
   "couple the repos" work. Needs its own migration plan + check-in before execution.

(W1–W3 are all independent of W4 and can ship in the current two-repo layout; W4 then folds them in.)
