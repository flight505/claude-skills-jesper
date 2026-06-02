# PLAN — Unify forge + catalog into one self-consistent system

> Execution plan for the locked decisions in `TODO.md` (D1–D6, 2026-06-01).
> Spans two repos today: **forge** (`~/Projects/Dev_projects/Claude_SDK/forge`, Go) and
> **this repo** (`claude-skills-jesper`, Python + content). SG4 merges them.
> Author/owner: Jesper. Reviewers in-loop: `cs-senior-engineer` (architecture) + `/code-review`
> (every forge diff). **Forge is personal-only** — this is why the end state is one repo.

---

## 1. North-star goal (single sentence)

**forge and its catalog are one repo with a pinned shared glossary, a first-class `category`
axis across *all* item types, and a non-breaking rename of the default source to `forge-market` —
such that every existing downstream `.forge.json` (sparkpad et al.) still `forge sync`s untouched,
and a teammate can clone the single repo and be productive with zero cross-repo knowledge.**

Everything below exists only to make that sentence true and *verified*.

---

## 2. Hard verification gate — the definition of "done"

The goal is **done** only when this whole gate is green, run from a **fresh clone of the merged
repo**. Treat it as one script (`scripts/verify-unification.sh`, authored in SG4); until the merge,
run the forge-side and catalog-side halves in their respective repos.

| # | Gate | Exact check | Hard? |
|---|---|---|---|
| **G1** | forge builds | `make build` exits 0 | ✅ blocking |
| **G2** | forge tests pass | `make test` (`go test ./...`) all green | ✅ blocking |
| **G3** | forge lints clean | `make lint` (`gofmt -l .` empty + `go vet ./...`) clean — OR the one known `testing.Chdir`/go1.24 vet warning explicitly waived in writing | ✅ blocking |
| **G4** | marketplace regenerates idempotently | `python3 scripts/regenerate-marketplace.py` then `git diff --exit-code .claude-plugin/marketplace.json` = no diff | ✅ blocking |
| **G5** | **downstream survives untouched** | In a real project whose committed `.forge.json` still says `source: "claude-skills-jesper"` (use sparkpad), `forge sync` restores every item green **with zero edits to that file** (`git -C <proj> diff --exit-code .forge.json`) | ✅ blocking — the whole point of D3 |
| **G6** | category axis works across types | `forge list --category <d>` and `forge search --category <d>` return items spanning ≥2 types; TUI shows a category filter; **every** catalog item carries a `category` (0 uncovered) | ✅ blocking |
| **G7** | glossary is single-sourced | The `## Glossary` block is **byte-identical** in forge README + forge CLAUDE.md (`diff <(extract) <(extract)` empty) | ✅ blocking |
| **G8** | fresh-clone round-trip | Clone merged repo → `make install` → `forge init` in a temp project → `forge install <item>` writes loadout → `forge sync` restores → `forge status` shows no drift | ✅ blocking |
| **G9** | sign-offs recorded | `/code-review` run + findings resolved on every forge diff (SG1–SG4); `cs-senior-engineer` PASS on the SG4 migration design **and** post-merge | ✅ blocking |

If any gate is red, the goal is not done — return to the owning sub-goal.

---

## 3. Operating rules (apply to every sub-goal)

1. **Loop to green.** A sub-goal isn't complete until its acceptance checks pass. Implement → run
   checks → if red, fix the smallest thing → re-run. No moving on with a red check.
2. **Test-first where it's code** (Jesper's global rule §4). For each forge behavior change, write
   the failing test that encodes the acceptance criterion *first*, then make it pass. The forge
   repo already has the pattern (`manifest_write_test.go`, `t.Chdir`).
3. **Surgical** (global rule §3). Every changed line traces to this plan. No drive-by refactors;
   note unrelated dead code, don't delete it.
4. **`/code-review` on every forge diff** before it merges to `main` — low/medium effort for the
   small ones (SG1, SG2, SG3), `high` for SG4. Resolve findings, then re-run until clean.
5. **`cs-senior-engineer` for structural calls** — spawn it to (a) review the `aliases` resolution
   design (SG2), (b) ratify the canonical category taxonomy (SG3), (c) **own the SG4 migration
   plan and review the result**. It is the architecture gate; `/code-review` is the line-level gate.
6. **Branch, never commit to `main` directly** (global workflow default). One branch per sub-goal.
7. **WARN before any action that incurs extra Claude usage** (Jesper's identity rule). Cloud
   `/code-review ultra` is billed — only on explicit say-so; default to local `/code-review`.
8. **Idempotency is sacred.** After any change touching `skills/`, `agents/`, `plugins/`,
   `upstream/`, run `regenerate-marketplace.py` and commit `marketplace.json` (repo convention).

---

## 4. Sub-goals (ordered; each loops to green before the next)

> Sequence rationale: glossary defines the words SG2–SG4 use → the alias resolver must exist before
> any rename is safe → category is independent data+UI work → the merge folds the finished pieces in
> and is the riskiest, so it goes last with full architecture oversight.

### SG1 — Pin & publish the glossary  · repo: forge · size: S

**Why first:** SG2–SG4 prose and code comments must use one vocabulary. Cheap, unblocks everything.

**Steps**
1. Lift the canonical glossary table from `TODO.md` (D4).
2. Add an identical `## Glossary` block to forge `README.md` and a new forge `CLAUDE.md`.
3. Fix `internal/cli/init.go:79` help text: `"manifest"` → `"loadout"` (sole code/term mismatch).
4. Surface the 3–4 load-bearing terms (loadout, source, catalog, surface) in `forge guide` output.

**Acceptance (loop to green)**
- [ ] G7 passes: glossary byte-identical in README + CLAUDE.md.
- [ ] `grep -rn "manifest" internal/cli/init.go` no longer describes `.forge.json` as a manifest.
- [ ] G1+G2+G3 still green (the init.go string change breaks nothing).

**Reviews:** `/code-review` (low) on the init.go diff. No senior-engineer needed (docs + 1 string).

---

### SG2 — Source aliases + rename to `forge-market`  · repo: forge · size: M

**Why second:** the alias resolver is the prerequisite that makes both the rename *and* the SG4
merge non-breaking for downstream `.forge.json`. Decided mechanism = Homebrew `formula_renames`
pattern (per-source `aliases: []`), the only family that needs zero downstream edits.

**Steps**
1. **Resolver first (release before any rename):**
   - Add `Aliases []string \`json:"aliases,omitempty"\`` to `RegistryEntry`
     (`internal/catalog/registry.go:13`).
   - In `resolveSourcePath` (`internal/installer/installer.go:159`) **and** `resolveMarketplaceRoot`
     (`installer.go:181`): when `items[].source` matches no source `id`, scan each source's
     `Aliases` and resolve.
   - **Test-first:** a `.forge.json` with `source:"oldname"` resolves to a source declaring
     `aliases:["oldname"]`; a non-matching source still errors as before.
2. **Then rename (one change):** flip the source `id` → `forge-market` and add
   `"aliases":["claude-skills-jesper"]` together, across the blast radius:
   `registry.go` ×6 (the `ID`, 2 dev-path probes, the `URL`), `internal/surfaces/cowork_test.go`,
   `~/.forge/sources.json`, `~/.claude/settings.json`.
   - GitHub repo-rename redirect makes the `URL:` change low-risk; still update it explicitly and
     never let the old repo name be re-squatted.

**Acceptance (loop to green)**
- [ ] New test: old-id `.forge.json` resolves via alias → PASS; no-match → still errors.
- [ ] G5 (manual, real): sparkpad's untouched `.forge.json` (`source: claude-skills-jesper`)
      `forge sync`s green; `git -C sparkpad diff --exit-code .forge.json` clean.
- [ ] G1+G2+G3 green; `cowork_test.go` updated and passing.
- [ ] **Order invariant honored:** resolver committed/releasable *before* the id flip (don't ship
      a rename a pre-alias forge can't resolve).

**Reviews:** `cs-senior-engineer` reviews the resolution design *before* coding (is `aliases` on the
source the right seam, or does it belong in a migrations map? — plan says source-field; confirm).
`/code-review` (medium) on the implemented diff.

---

### SG3 — `category` as a first-class axis across all types  · repos: this + forge · size: M

**Correction baked in:** `forge list --category` **already exists** (`internal/cli/list.go:18,51,67`)
and `schemas.Item.Category` is populated. Axis is half-built; close the three gaps.

**Steps**
1. **Backfill data (this repo):**
   - First-party items: add `category:` to each `SKILL.md`/agent/plugin frontmatter
     (`regenerate-marketplace.py` already reads it).
   - Upstream non-plugins (0/27 agents, 0/38 commands, 0/7 personas, 0/10 skills) + 2 uncovered
     plugins: build a **committed domain-map file in *this* repo** (NOT in `upstream/`, which is
     never hand-edited) keyed by item name → category; teach `regenerate-marketplace.py` to apply
     it. Map must **survive `sync-upstream.sh`** (it lives outside `upstream/`).
2. **Normalize the taxonomy:** the 15 raw values (`development` 26, `leadership` 8, `research` 8,
   `productivity` 5, `product` 4, `marketing` 3 + 9 singletons: `compliance`, `project-management`,
   `business-growth`, `finance`, `design`, `knowledge`, `operations`, `commercial`, `research-ops`)
   collapse to a canonical ~8–10 set. `cs-senior-engineer` ratifies the final set.
3. **Extend the axis (forge):**
   - Add `--category` to `internal/cli/search.go` (one `StringVar` + a filter mirroring `--type`).
   - Add a `categoryFilter` + cycle to the TUI (`ui/views/catalog.go` has `typeFilter`, no category
     equivalent yet).

**Acceptance (loop to green)**
- [ ] G4: regenerate is idempotent; `marketplace.json` valid.
- [ ] G6: **every** catalog item carries a `category` (assert 0 uncovered across all 5 types,
      first-party included); `forge list --category X` and `forge search --category X` each return
      items spanning ≥2 types; TUI category filter works.
- [ ] G1+G2+G3 green; new forge tests cover the `search --category` filter.
- [ ] Re-run after a dry `sync-upstream.sh` preview: the domain-map still applies (survives pulls).

**Reviews:** `cs-senior-engineer` ratifies the canonical taxonomy (a design call with lock-in).
`/code-review` (medium) on the forge `search`/TUI diff.

---

### SG4 — Merge into one repo, vertical separation  · the migration · size: L · senior-engineer-led

**Decided (D1):** one repo, because forge is personal-only — no general-tool reason to split, and
separation has caused repeated drift + "agents forget the halves connect" confusion. The *whether*
is settled; **the *how* is a migration that `cs-senior-engineer` owns end-to-end.**

**Steps**
1. **`cs-senior-engineer` writes the migration plan first** (its own short doc), deciding the open
   mechanics:
   - Which repo's git history is the base vs. brought in as a subtree/merge (preserve both?).
   - Target layout (illustrative): `forge/{cmd,internal,ui}` for the tool, `forge/catalog/{upstream,
     skills,agents,plugins,scripts,.claude-plugin}` for content, one `CLAUDE.md` + `README.md`.
   - Where forge's **default-source path** points post-merge (in-repo relative path vs. still a
     named `forge-market` source) — must keep G5 true.
   - CI/release: tool binary build vs. `regenerate-marketplace.py` in one tree.
   - `git subtree` for `upstream/` survives inside the monorepo (it's designed for this).
2. **Execute** per that plan, on a branch, in a throwaway clone first.
3. **Fold in SG1–SG3 artifacts:** single glossary now lives in the one CLAUDE.md/README; the
   `forge-market` source either stays a named source or becomes the in-repo default.
4. **Author `scripts/verify-unification.sh`** = the §2 gate G1–G8 as one runnable script.

**Acceptance (loop to green)**
- [ ] Full §2 gate G1–G9 green from a **fresh clone** of the merged repo.
- [ ] G5 still holds post-merge: downstream `.forge.json` (old source id) syncs untouched.
- [ ] Both repos' histories preserved per the migration plan (no force-lost history).
- [ ] `cs-senior-engineer` PASS on the merged result; `/code-review high` clean.

**Reviews:** `cs-senior-engineer` owns design + result. `/code-review` at `high`. (Offer
`/code-review ultra` only if Jesper asks — it's billed; warn first.)

---

## 5. Sequence & dependencies

```
SG1 glossary ─┐
              ├─► SG4 monorepo merge ─► §2 GATE (G1–G9) ─► GOAL ✅
SG2 alias ────┤        (cs-senior-engineer led)
SG3 category ─┘
```

- SG1, SG2, SG3 are mutually independent and all ship in the **current two-repo layout**.
- SG4 is **blocked by** SG1+SG2+SG3 (it folds their finished artifacts in) and is the only one that
  touches both repos at once. Matches the task graph: W4 `blockedBy` W1, W2, W3.
- Within SG2, the **resolver must precede the rename** (hard ordering invariant).

---

## 6. Safety / rollback

- Every sub-goal on its own branch; nothing lands on `main` without its acceptance + `/code-review`.
- SG2's alias entry is kept **forever** (cost ≈ nothing) so un-migrated downstreams never break;
  any `.forge.json` rewrite is opt-in only (`forge migrate`), **never silent**.
- SG4 rehearsed in a throwaway clone before touching the real repos; histories preserved.
- G5 is re-checked after SG2 *and* after SG4 — the downstream-untouched guarantee is the canary.

---

## 7. Where the agents plug in (summary)

| Sub-goal | `cs-senior-engineer` | `/code-review` |
|---|---|---|
| SG1 glossary | — | low (init.go string) |
| SG2 alias+rename | design review (is `aliases` the right seam?) **before** coding | medium |
| SG3 category | **ratify canonical taxonomy** | medium (search/TUI) |
| SG4 merge | **owns migration plan + reviews result** | high |

---

## Appendix A — Ratified category taxonomy (SG3, cs-senior-engineer)

**9 canonical categories** (slug = machine value *and* display label; no separate human field):
`engineering` · `product` · `marketing` · `leadership` · `research` · `finance` · `operations`
· `compliance` · `productivity`.

**Raw → canonical collapse** (applied as a normalization pass in `regenerate-marketplace.py`, so
future upstream items carrying old values are remapped automatically):
`development→engineering`, `project-management→operations`, `business-growth→operations`,
`design→product`, `knowledge→productivity`, `commercial→finance`, `research-ops→research`;
`leadership`, `research`, `productivity`, `product`, `marketing`, `compliance`, `finance`,
`operations` retained.

**Assignment for uncovered items** (agents/commands/personas + first-party): (1) inherit the parent
plugin's category if bundled; else (2) name/description keyword match; else (3) fallback
`productivity`. Cross-cutting rule: categorize by *primary consumer's outcome*, not subject matter
(e.g. `skill-security-auditor`→`engineering`, doc-skills→`productivity`).

**Storage:** upstream non-plugin assignments live in a committed `scripts/upstream-category-map.json`
(name→category) the generator applies — never edited into `upstream/`. First-party items get
`category:` frontmatter; the generator warns (not fails) on a missing one, defaulting `productivity`.

Status: taxonomy **ratified**; backfill (data) **pending sign-off**.

## 8. Provenance

Decisions: `TODO.md` (D1–D6). Research: krew/krew-index, Homebrew `formula_renames.json`/
`tap_migrations.json`, asdf, Helm + forge codebase audit (`list.go`, `search.go`, `installer.go`,
`registry.go`, `catalog.go`, `ui/views/catalog.go`). forge PR #18 (manifest write-path, Closes #17)
is the foundation SG2 builds on.
