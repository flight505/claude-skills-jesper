# TODO — architecture backlog

> The previous TODO.md tracked 7 implementation tracks (item-context chat, project-aware
> suggest, sources taxonomy, etc.) — **all shipped and merged**. Completed work lives in git
> history (`git log`; forge PRs #2–#11, this repo PRs #2–#8), so it's removed from this file.
> What remains are **open architectural decisions** about how `forge` and this marketplace
> relate. These are design questions — think before acting.

The two repos in play:
- **forge** (`flight505/forge`) — the Go CLI/TUI installer. Organizes everything by **what it
  is**: skill · plugin · agent · persona · command.
- **this repo** (`claude-skills-jesper`) — the content marketplace. `upstream/` (vendored
  `alirezarezvani/claude-skills`) + a thin first-party layer (`skills/`, `agents/`, `plugins/`),
  merged into `.claude-plugin/marketplace.json` by `scripts/regenerate-marketplace.py`.

---

## A1 — Shared nomenclature between forge and the marketplace

The two repos use **drifting vocabulary** for the same concepts. Pin one glossary, identical in
the forge README and this CLAUDE.md (and `forge guide`).

Terms needing a single canonical definition:
- **item / add-on / entry** — pick ONE word for "a thing in the catalog" (code says `Item`; docs
  drift between add-on / entry / item).
- **source** vs **catalog** vs **marketplace** — `source` = a registered provider; `catalog` =
  the merged in-memory view; `marketplace` = the on-disk `marketplace.json`. Stop interchanging.
- **loadout** (`.forge.json`) vs **manifest** — README says "loadout", code/file/commits say
  manifest. Pick one.
- **surface** — keep (forge's word for an install target).
- **type** (skill/plugin/…) vs **category / domain** (use-case) — two *different axes*; see A4.
  Never conflate them in prose.

Deliverable: a "Glossary" block, byte-identical in both repos.

---

## A2 — `claude-skills-jesper` is a poor, now-hardcoded folder name

"skills" implies a skills bucket, but the folder is the **marketplace** — it holds plugins,
agents, personas, commands *and* skills. It reads as unrelated to forge.

**Blast radius (why it's not a simple `mv`)** — the string is hardcoded in:
- `forge/internal/catalog/registry.go` — the default-source `ID: "claude-skills-jesper"`, two
  dev-path probes, and `URL: github.com/flight505/claude-skills-jesper`
- `~/.forge/sources.json` — source `id` + absolute `path`
- `~/.claude/settings.json`
- every downstream `.forge.json` → `items[].source: "claude-skills-jesper"` (e.g. sparkpad ×4)
- `forge/internal/surfaces/cowork_test.go` (test fixtures)

Decision needed — **rename or alias?**
- *Rename* (e.g. `forge-catalog` / `forge-marketplace`) is cleanest but must migrate the source
  id + the registry.go defaults + every downstream `source:` value, or `forge sync` breaks.
- *Alias* — teach forge a source `aliases: []` so the old id keeps resolving while the canonical
  id changes. Lower blast radius; small forge change.

Recommendation to evaluate: **add source-alias support in forge first**, then rename, so nothing
breaks mid-migration. The chosen name should reflect the A1 glossary (it's a *catalog/marketplace*,
not *skills*).

---

## A3 — forge ↔ marketplace are loosely coupled (no cross-doc; maybe shouldn't be 2 repos)

forge has **no CLAUDE.md**, and its README never mentions this marketplace; this repo points at
forge but forge doesn't point back. forge even hardcodes this repo as its default source
(registry.go) yet documents nothing about it. A newcomer can't tell they're two halves of one
system.

1. **Minimum fix:** add a forge CLAUDE.md + a README section naming this marketplace as the
   reference content source; cross-link both ways. Low effort, high clarity. Do regardless of #2.
2. **Bigger question:** should they be **one repo**? forge is the tool; this is its default
   content, and forge already hardcodes the path. Monorepo pros: single clone, no source-
   registration step, no name drift (subsumes A2), atomic tool+content changes. Cons: Go binary +
   vendored `upstream/` subtree in one tree; noisier subtree pulls; others can't take forge
   without the content. Treat as a real RFC — write the trade-offs before deciding; don't merge
   by default.

---

## A4 — Surface use-case **domains**, not just **types**

The core confusion. There are **two independent axes**; forge surfaces only one.

- **Type** (what it *is*): skill / plugin / agent / persona / command. ← forge groups by this.
- **Domain** (what it's *for*): the use-case field — Engineering, Marketing, Commercial, etc.

**Studied upstream + the generated catalog (2026-06-01) — accurate state:**
- Upstream's README groups its content into ~16 use-case domains (🔧 Engineering Core/POWERFUL,
  📣 Marketing, 💼 Commercial, 🏭 Business Operations, 📈 Business & Growth, 💰 Finance,
  🔬 Research, 🩺 Compliance, 🧠 Knowledge/Productivity, 🎓 Learning, leadership, product, …).
- **Domain *is* partly machine-readable already:** `upstream/.claude-plugin/marketplace.json`
  carries a `category` on **63/63** plugins (development 26, leadership 8, research 8,
  productivity 5, product 4, marketing 3, + singletons). `regenerate-marketplace.py` passes these
  through, so our generated `marketplace.json` has `category` on **62/65 plugins**.
- **The gap:** category is plugin-only. In the generated catalog, **0 of** the 27 agents, 38
  commands, 7 personas, and 10 skills carry a `category` — and the 3 uncategorized plugins +
  **all first-party items** have none either. `schemas.Item` *has* a `Category` field and
  `regenerate-marketplace.py` *does* read frontmatter `category:` — it's just unset for non-plugins
  and first-party.
- **forge ignores the axis even where it exists:** no `forge list --category`, no domain grouping
  in TUI/CLI. The 62 categorized plugins can't be browsed by domain today.
- **First-party compounds it:** first-party items are filed by *type* (`skills/`, `agents/`,
  `plugins/`), so a personally-authored engineering agent and engineering plugin share no
  "Engineering" grouping.

**Goal:** browse/filter the catalog by **domain** as a first-class axis, across all types and both
upstream + first-party — *without* moving anything out of the type-based folders (the install layer
depends on them).

Design directions to evaluate (don't pick yet — needs a design pass):
1. **Backfill `category` for the uncovered set.** First-party: add `category:` to frontmatter
   (regenerate already reads it). Upstream non-plugin items: derive from a **committed domain map**
   in *this* repo (not in `upstream/`, which is never hand-edited) keyed off the README's
   domain→item assignment; `regenerate-marketplace.py` applies it.
2. **forge gains a domain axis:** `forge list --category <d>` / `forge search` domain filter / a
   TUI "Domains" grouping — reads the existing `category` field, so categorized plugins work
   immediately and improve as backfill lands.
3. **Normalize the vocabulary** — upstream's `category` values (e.g. `development`) vs the README's
   prose domains (e.g. "Engineering") don't match 1:1. Pick a canonical domain set (ties to A1)
   and map both into it.

Constraints: don't break the type-based install dirs; the domain map must survive
`sync-upstream.sh`; keep `category` (machine field) and the canonical domain label consistent.

**Prereq before coding:** transcribe the upstream README's domain→item assignment into a committed
map file (only the ~16 domain headers are captured so far; per-item assignment for the non-plugin
types still needs doing).

---

## Sequencing

A1–A4 interlock. Suggested order: **A1** (glossary; defines type vs domain) → **A4** (domain
model — the substantive feature, and where the glossary earns its keep) → **A3** (cross-docs /
one-repo RFC, incorporating the glossary + domain model) → **A2** (rename last, behind alias
support so nothing breaks).
