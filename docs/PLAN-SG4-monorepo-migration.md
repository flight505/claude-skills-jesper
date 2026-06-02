# PLAN — SG4: Monorepo Migration (forge absorbs catalog)

> Owner: Jesper / `cs-senior-engineer`. Execute in a later session — this document is **plan only**.
> Every step that cannot be undone is marked **[IRREVERSIBLE]**.
> Context: `PLAN-forge-unification.md` §4 SG4.

---

## 0. Decisions locked by this plan

| # | Decision | Rationale |
|---|---|---|
| D-M1 | **Base repo = forge.** Catalog is brought in via `git subtree add`. | forge has the CI, release pipeline, and Go module; catalog's content fits cleanly as a subtree prefix. Avoids re-establishing CI/GoReleaser from scratch. |
| D-M2 | **Mechanism = `git subtree add --prefix=catalog <catalog-remote> main --squash`.** | Preserves both histories in one DAG without rewriting any commit SHA. `git-filter-repo` is not installed and would rewrite catalog SHA history, making the upstream subtree inside catalog unfindable by `git subtree pull`. Squash means one tidy merge commit. |
| D-M3 | **Upstream subtree inside catalog: works as-is, prefix updated to `catalog/upstream`.** | `git subtree pull --prefix=catalog/upstream` is the only change needed. The squashed upstream history arrives intact inside the outer squash commit; subsequent pulls continue to work because `git subtree` tracks the split by the prefix annotation in commit messages, which survive. |
| D-M4 | **Default source post-merge = in-repo local path `catalog/` relative to the forge repo root.** | After PR #20 (forge-market rename) merges, `defaultRegistry()` already probes `~/Projects/Dev_projects/Claude_SDK/claude-skills-jesper`. Post-merge, a second probe for `…/forge/catalog` is added. The remote fallback stays pointing at the *GitHub repo URL* (unchanged until the optional repo-archive step). G5 is preserved because `item.Source` is stamped from the registered source id, which PR #20's `migrateSourceIDs` keeps working for any `source: claude-skills-jesper` in downstream `.forge.json`. |
| D-M5 | **`marketplace.json` `name` field stays `claude-skills-jesper`.** | Downstream `enabledPlugins` keys (e.g. `code-cleanup@claude-skills-jesper`) are keyed to this string. Renaming it silently breaks every Cowork installation. Repo name ≠ marketplace name ≠ forge source id — these are three independent namespaces. |
| D-M6 | **Merge all open PRs first, then cut the monorepo.** | Gives a clean, tested base. Rebasing post-migration is error-prone because the directory tree changes under the branch. |
| D-M7 | **CI = one workflow file, path-filtered jobs.** | The existing `ci.yml` covers Go; a new `catalog.yml` workflow fires only on `catalog/**` changes. `release.yml` is unchanged (tags trigger the whole-repo GoReleaser job; catalog content ships in the `catalog/` tree that rides along in the source archive). |

---

## 1. Pre-flight checklist (before any git mutation)

Work through this list top-to-bottom, in a terminal, against the real repos. All items are read-only or in throwaway clones — nothing irreversible yet.

### 1.1 Merge all open PRs

All five branches were cut from `main` and are **independent** (SG2 dropped the alias
resolver, so there is no resolver-before-rename ordering constraint). Merge in any order;
ascending PR number is tidy. They must all be on their repo's `main` before the cut.

1. **forge PR #18** — `feat/manifest-write-path` (the install/remove→`.forge.json` fix; Closes #17).
2. **forge PR #19** — `feat/glossary` (**SG1**).
3. **forge PR #20** — `feat/source-rename-forge-market` (**SG2** — `forge-market` + legacy-id migration).
4. **forge PR #21** — `feat/search-category` (**SG3** forge axis — `list`/`search`/TUI `--category`).
5. **catalog PR #9** — `feat/category-backfill` (**SG3** data — the 9-category backfill).

After each merge, verify:
```bash
# forge: all green
cd /Users/jesper/Projects/Dev_projects/Claude_SDK/forge
make build && make test && make lint

# catalog: idempotent regeneration
cd /Users/jesper/Projects/Dev_projects/Claude_SDK/claude-skills-jesper
python3 scripts/regenerate-marketplace.py
git diff --exit-code .claude-plugin/marketplace.json
```

**Stop.** Do not proceed to §1.2 if any gate is red.

### 1.2 Rehearsal in a throwaway clone

This step is mandatory — it proves the exact commands before touching the real forge repo.

```bash
# Create throwaway copies (copies, not clones, so no remote push is possible)
cd /tmp
cp -R /Users/jesper/Projects/Dev_projects/Claude_SDK/forge forge-rehearsal
cp -R /Users/jesper/Projects/Dev_projects/Claude_SDK/claude-skills-jesper catalog-rehearsal

# Give the catalog copy a file-based remote so git subtree add can reach it
cd catalog-rehearsal
git init --bare /tmp/catalog-rehearsal-bare
git remote add tmp-remote /tmp/catalog-rehearsal-bare
git push tmp-remote main

# Run the merge (see §2 for the real commands — run them here first)
cd /tmp/forge-rehearsal
git remote add catalog-remote /tmp/catalog-rehearsal-bare
git fetch catalog-remote main
git subtree add --prefix=catalog catalog-remote/main --squash \
    -m "chore(monorepo): absorb catalog as catalog/ subtree"

# Verify structure
ls catalog/
ls catalog/upstream/
ls catalog/scripts/
ls catalog/.claude-plugin/

# Verify history of both sides is visible
git log --oneline | head -15
git log --oneline catalog/ | head -5

# Run Go build (proves no Go files broke)
make build && make test && make lint

# Verify marketplace regenerates (Python scripts must resolve paths correctly — see §3)
python3 catalog/scripts/regenerate-marketplace.py
diff <(python3 catalog/scripts/regenerate-marketplace.py --dry-run) \
     catalog/.claude-plugin/marketplace.json && echo "idempotent"
```

If the rehearsal passes cleanly, proceed to §2.

---

## 2. The merge — exact commands

**[IRREVERSIBLE from step 2.3 onward]** — steps 2.1–2.2 are read-only.

### 2.1 Add catalog as a remote in the forge repo

```bash
cd /Users/jesper/Projects/Dev_projects/Claude_SDK/forge

# Add the catalog repo as a named remote. This is read-only and reversible
# (git remote remove catalog-source removes it).
git remote add catalog-source \
    https://github.com/flight505/claude-skills-jesper.git
git fetch catalog-source main
```

### 2.2 Verify the fetch

```bash
git log --oneline catalog-source/main | head -5
# Must show: "9628b3c feat(category): backfill category across all item types (SG3)"
# (or the PR #9 merge commit if it landed after 9628b3c)
```

### 2.3 Absorb catalog as `catalog/` subtree [IRREVERSIBLE]

This creates a merge commit that grafts the catalog's entire history into the forge DAG under `catalog/`.

```bash
# Confirm forge main is clean before the merge
git status          # must be clean
git log --oneline -1  # note the SHA — this is the rollback point

# The merge
git subtree add --prefix=catalog catalog-source/main --squash \
    -m "chore(monorepo): absorb claude-skills-jesper as catalog/ (SG4)"
```

After this command, `catalog/` is populated and a merge commit exists. **This is the first irreversible step** — it rewrites `forge/main`'s linear history. (Recoverable via `git reset --hard <pre-merge-sha>` *before* pushing, but irreversible once pushed.)

### 2.4 Verify raw structure

```bash
ls catalog/
# Expected: agents  docs  plugins  scripts  skills  upstream  CLAUDE.md  README.md  TODO.md  .claude-plugin

ls catalog/upstream/ | head -5        # upstream subtree content present
ls catalog/scripts/                   # all Python scripts present
ls catalog/.claude-plugin/            # marketplace.json present

git log --oneline | head -5           # merge commit is HEAD
git log --oneline catalog/ | head -5  # catalog history visible
```

---

## 3. Fix-ups (after merge, before pushing)

All changes in this section happen on a branch cut from the post-merge `main`. Do not push `main` yet.

```bash
git checkout -b feat/sg4-monorepo-fixups
```

### 3.0 [CRITICAL — do this first] Fence `catalog/` out of the Go module

**Found in rehearsal (2026-06-02):** `catalog/upstream/` ships Go *skeleton assets*
(e.g. `…/kubernetes-operator/assets/reconcile_skeleton.go`) with placeholder imports
like `<MODULE>/api/v1alpha1`. Once `catalog/` lives inside forge's Go module, `go build
./...` / `go test ./...` / `go vet ./...` descend into it and **fail with exit 1**
(`invalid import path: <MODULE>/...`). G1–G3 are red without this fix.

Fix (proven in rehearsal): add a stub nested module so Go's `./...` skips the whole
subtree. A directory with its own `go.mod` is a separate module and excluded from the
parent's `./...`.

```bash
printf 'module catalog-content\n\ngo 1.23\n' > catalog/go.mod
go build ./...   # now exits 0
go test ./...    # now passes
```

This `catalog/go.mod` is sacrificial — nobody builds `catalog-content`; it exists purely
to fence the non-compilable skill assets out of forge's build. Commit it as part of the
fix-ups. (Alternative considered & rejected: renaming to `_catalog`/`.catalog` — Go skips
those too, but `catalog/` is the wanted name and breaks every doc path.)

### 3.1 Update `defaultRegistry()` — add the in-repo probe

File: `internal/catalog/registry.go`

The function `defaultRegistry()` currently probes two paths (after PR #20 lands):
```
~/Projects/Dev_projects/Claude_SDK/claude-skills-jesper
~/claude-skills-jesper
```

Add a third probe **before** the existing two, pointing at the in-repo `catalog/` directory relative to the forge binary/repo:

```go
// New probe: in-repo path (monorepo layout — forge/catalog/)
filepath.Join(platform.Home(), "Projects", "Dev_projects", "Claude_SDK", "forge", "catalog"),
```

Rationale for ordering: the in-repo path should win over the old standalone-repo path (more specific). The existing two paths remain as fallbacks for machines where the old layout persists. The remote fallback (github.com/flight505/claude-skills-jesper) remains last and unchanged.

No other change to `registry.go`. The `legacySourceIDs` migration map (`claude-skills-jesper` → `forge-market`) from PR #20 is already in place and handles downstream `.forge.json` files — do not modify it.

**Verify:** `make build && make test` green. Spot-check with `forge list` from inside the forge repo (it should find `catalog/.claude-plugin/marketplace.json`).

### 3.2 Update `scripts/sync-upstream.sh` — prefix change

The script currently sets `PREFIX="upstream"` and runs:
```bash
git subtree pull --prefix="$PREFIX" "$REMOTE_NAME" "$REF" --squash
```

After the merge, the subtree lives at `catalog/upstream`, not `upstream`. Change line 18:

```bash
PREFIX="catalog/upstream"
```

The dirty-check on line 33 uses `$PREFIX` already, so it automatically guards the right tree:
```bash
if [[ -n "$(git status --porcelain -- upstream/)" ]]; then
```
→ becomes `catalog/upstream/` automatically.

The `REPO_ROOT` derivation (`cd "$(dirname "$0")/.." && pwd`) will resolve to `catalog/` once the script lives at `catalog/scripts/sync-upstream.sh`. At that point `REPO_ROOT` is the catalog subtree root, which is correct for all git operations that pass `-C "$REPO_ROOT"` — **but** `git subtree pull` must run against the forge repo root (the outer repo), not the catalog subtree root, because the subtree annotation lives in the outer DAG.

Fix: change the `git subtree pull` line to explicitly use the outer repo root:

```bash
OUTER_ROOT="$(cd "$REPO_ROOT/.." && pwd)"
# ...
git -C "$OUTER_ROOT" subtree pull --prefix="$PREFIX" "$REMOTE_NAME" "$REF" --squash \
    -m "chore: sync upstream alirezarezvani/claude-skills@$REF"
```

And similarly change the dirty-check:
```bash
if [[ -n "$(git -C "$OUTER_ROOT" status --porcelain -- "$PREFIX/")" ]]; then
```

All other `git remote` and `git fetch` invocations in the script also need `-C "$OUTER_ROOT"` because they act on the outer repo's remote list. The `python3 scripts/regenerate-marketplace.py` call stays relative to `REPO_ROOT` (catalog root) — correct.

### 3.3 Python scripts — path audit

All four Python scripts use `ROOT = Path(__file__).resolve().parent.parent`.

| Script (path after merge) | `__file__` resolves to | `parent.parent` resolves to | Correct? |
|---|---|---|---|
| `catalog/scripts/regenerate-marketplace.py` | `catalog/scripts/regenerate-marketplace.py` | `catalog/` | Yes — all paths (`UPSTREAM_DIR`, `SKILLS_DIR`, etc.) are relative to `catalog/` which is correct |
| `catalog/scripts/upstream-changelog.py` | `catalog/scripts/upstream-changelog.py` | `catalog/` | Yes — `ROOT` used only for `git -C str(ROOT)` calls; resolves to catalog subtree root, which is fine because `git -C catalog/` sees the outer repo and the `upstream/` prefix is interpreted relative to the outer repo |
| `catalog/scripts/check-sources.py` | `catalog/scripts/check-sources.py` | `catalog/` | Yes — `SKILLS_DIR`, `AGENTS_DIR`, `PLUGINS_DIR` are all under `catalog/`; the `git remote get-url upstream-skills` call uses `-C str(ROOT)` = catalog dir, which git will walk up to find the outer repo. |
| `catalog/scripts/upstream-category-map.json` | Not a script; data file. | n/a | No change needed. |

**The only script with a subtlety is `upstream-changelog.py`:** it calls `git -C str(ROOT)` where `ROOT = catalog/`. Git will walk up to the outer repo root automatically (git always walks up to find `.git`), so the remote and log commands resolve against the forge repo. The `PREFIX = "upstream/"` constant in `upstream-changelog.py` must be updated to `"catalog/upstream/"` to match the new subtree prefix.

```python
# upstream-changelog.py line 19 (approximately)
PREFIX = "catalog/upstream/"
```

### 3.4 `skills/_shared/install-refresh-daemons.sh` — repo root derivation

Current line 26:
```bash
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
```

After move to `catalog/skills/_shared/install-refresh-daemons.sh`:
- `dirname "${BASH_SOURCE[0]}"` = `catalog/skills/_shared`
- `../..` = `catalog/`

That is correct: `REPO_ROOT` should point to `catalog/` (the content root, not the outer forge root). Line 50 `"$REPO_ROOT/skills/"*/` resolves to `catalog/skills/*/` — correct. Line 72's `cd '$REPO_ROOT/skills/${name}'` — correct.

No change needed.

### 3.5 Single `CLAUDE.md` and `README.md`

The merged repo will have:
- `CLAUDE.md` (forge's — the outer repo file)
- `catalog/CLAUDE.md` (catalog's — inside the subtree)
- `README.md` (forge's)
- `catalog/README.md` (catalog's)

**Do not delete catalog's inner docs** — they are correct for anyone navigating the catalog subtree. Instead, add a short `## Catalog` section to forge's top-level `CLAUDE.md` and `README.md` pointing at `catalog/CLAUDE.md` for catalog-specific conventions. The SG1 glossary (already identical in both docs post-PR #19) continues to live at the top level; `catalog/CLAUDE.md` can reference up to it.

This is a prose-only change — no logic impact.

### 3.6 Verify fix-ups compile and regenerate

```bash
# From forge repo root
make build && make test && make lint

# From catalog subtree root
python3 catalog/scripts/regenerate-marketplace.py
git diff --exit-code catalog/.claude-plugin/marketplace.json
```

### 3.7 Add catalog CI workflow

Create `.github/workflows/catalog.yml`:

```yaml
name: catalog

on:
  push:
    branches: [main]
    paths: ['catalog/**']
  pull_request:
    paths: ['catalog/**']

jobs:
  regenerate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Regenerate marketplace.json
        run: python3 catalog/scripts/regenerate-marketplace.py
      - name: Assert idempotent
        run: git diff --exit-code catalog/.claude-plugin/marketplace.json
```

The existing `ci.yml` (Go build/test/lint) fires on all pushes and PRs — no path filter needed there (Go changes can be anywhere).

### 3.8 Commit fix-ups and open PR

```bash
git add internal/catalog/registry.go
git add catalog/scripts/sync-upstream.sh
git add catalog/scripts/upstream-changelog.py
git add .github/workflows/catalog.yml
git add CLAUDE.md README.md     # prose additions only
git commit -m "chore(sg4): monorepo fix-ups — registry probe, sync prefix, script paths, catalog CI"

# Open PR against main
gh pr create \
  --title "chore(sg4): monorepo fix-ups after catalog/ subtree merge" \
  --body "Fix-ups required post SG4 merge: registry default probe, sync-upstream prefix, upstream-changelog prefix constant, catalog CI workflow. Pairs with the SG4 subtree merge commit."
```

---

## 4. Verification gate

Run from a **fresh clone** of the merged repo. All gates must be green before declaring SG4 done.

```bash
# Fresh clone
git clone https://github.com/flight505/forge /tmp/forge-verify
cd /tmp/forge-verify
```

| Gate | Command | Pass criterion |
|---|---|---|
| **G1** build | `make build` | exits 0 |
| **G2** tests | `make test` | all green |
| **G3** lint | `make lint` | exits 0 (or the known `testing.Chdir`/go1.24 vet warning explicitly waived) |
| **G4** marketplace idempotent | `python3 catalog/scripts/regenerate-marketplace.py && git diff --exit-code catalog/.claude-plugin/marketplace.json` | no diff |
| **G5** downstream untouched | In a real project whose `.forge.json` has `source: "claude-skills-jesper"`, run `forge sync`; then `git -C <project> diff --exit-code .forge.json` | no diff |
| **G5-b** in-repo source resolves | From the fresh clone dir, run `forge list` (no arguments); verify items appear from `catalog/.claude-plugin/marketplace.json` | items listed, no "source not found" error |
| **G6** category axis | `forge list --category engineering` returns items spanning ≥ 2 types | multi-type results |
| **G7** glossary identical | `diff <(grep -A20 "## Glossary" README.md) <(grep -A20 "## Glossary" catalog/CLAUDE.md)` | empty diff (or both reference the same glossary location) |
| **G8** fresh clone round-trip | `make install && forge init /tmp/tproj && forge install cs-senior-engineer --project /tmp/tproj && forge sync --project /tmp/tproj && forge status --project /tmp/tproj` | no drift |
| **G9** sign-offs | `/code-review high` run on the fix-ups PR; findings resolved; `cs-senior-engineer` PASS recorded | both green |
| **G-sync** upstream sync works | `cd /tmp/forge-verify && bash catalog/scripts/sync-upstream.sh --dry-run` | exits 0, shows upstream diff preview, no "prefix not found" error |

---

## 5. Rollback

### Before pushing (post §2.3, pre §2.4-push)

The merge commit is local only. Roll back with:

```bash
# Note: SHA recorded in step 2.3 above
git reset --hard <pre-merge-sha>
git remote remove catalog-source
```

Both repos are completely unaffected — the catalog repo was never touched.

### After pushing to GitHub but before merging fix-ups PR

Revert the merge commit:

```bash
git revert -m 1 <merge-commit-sha>
git push origin main
```

The catalog subtree merge commit has two parents; `-m 1` keeps the mainline (forge). This is a forward-commit revert, not history destruction.

### After the fix-ups PR merges

If a critical bug is found post-merge, the fix-ups PR can be reverted first (standard `git revert`), then the subtree merge commit reverted with `-m 1`. The catalog repo is always intact — it was never modified.

### Restoring independent repos (worst case)

The catalog repo was never modified during this migration. To restore the pre-merge state of forge:

```bash
cd forge
git log --oneline | grep "absorb claude-skills-jesper"   # find the merge SHA
git reset --hard <sha-before-merge>
git push origin main --force-with-lease   # requires Jesper's approval; warn first
```

This is the nuclear option — `force-with-lease` is destructive to collaborators (there are none for this personal repo, but note it anyway).

---

## 6. Open risks / what could go wrong

0. **[CONFIRMED in rehearsal] `catalog/upstream` Go skeleton assets break `go build ./...`.** Two `*.go` skill-template files carry placeholder imports (`<MODULE>/...`). Inside forge's module they fail the build/test/lint gates. **Fixed** by §3.0 (stub `catalog/go.mod`); verified `go build ./...` + `go test ./...` pass after. Must be applied immediately after the merge, before any gate run.

1. **`git subtree add --squash` and nested subtrees.** The `upstream/` subtree inside catalog was itself pulled with `--squash`. After the outer `--squash` absorb, `git subtree pull --prefix=catalog/upstream` must re-discover the split point via the commit message annotation. The annotation format is `Squashed 'catalog/upstream/' changes from ...` — but the squash commit in the inner catalog repo says `Squashed 'upstream/' changes from ...`. Git subtree uses this to find the split; the prefix mismatch means **git subtree will not find the old annotation** and may error on the first `sync-upstream.sh` run post-merge. Mitigation: after the merge, run one `git subtree pull --prefix=catalog/upstream catalog-source-upstream main --squash` to lay down a new annotation with the correct prefix. Document this as a one-time bootstrap step in `catalog/scripts/sync-upstream.sh`.

2. **`upstream-skills` remote lives in the catalog repo, not forge.** After the merge, `sync-upstream.sh` needs the `upstream-skills` remote to exist in the outer (forge) repo. It will not — only `catalog-source` will be there. The script adds it if missing (lines 39–42 of the current script), so this is handled automatically on first `sync-upstream.sh` run. Confirm the add-if-missing logic survives the script edits in §3.2.

3. **`catalog-source` remote left in forge.** After the merge, this remote is unnecessary (the subtree is in-tree). Remove it post-merge to avoid confusion: `git remote remove catalog-source`. Add this as a cleanup step after §2.3.

4. **PR #20's `defaultRegistry()` still probes the old `claude-skills-jesper` path.** After the monorepo merge, a developer machine may have both paths: `…/claude-skills-jesper` (old standalone repo, possibly archived/deleted) and `…/forge/catalog`. If the old path still exists with a valid `marketplace.json`, it will win (it comes first in the probe list). Fix: reorder the probes in §3.1 so `…/forge/catalog` is checked first.

5. **GoReleaser source archives include `catalog/`.** The `.goreleaser.yaml` `archives` section lists `files: [README.md, LICENSE, MIGRATION.md]`. It does not glob `catalog/`. This is fine for the binary release, but means the source archive won't ship catalog content. For a personal tool this is acceptable; if needed, add `catalog/` to the `files` list. Not a blocker.

6. **`make install` runs `web` target first.** The `web` target requires `pnpm` and Node. This is unrelated to the catalog merge but worth noting: the install target silently skips the web build if pnpm is absent (`|| true`). The Go binary still builds. No catalog impact.

7. **GitHub redirect lag after repo rename (if catalog repo is archived/renamed later).** The `defaultRegistry()` remote fallback URL (`https://github.com/flight505/claude-skills-jesper`) will redirect to the new name via GitHub's redirect. Do not rename the catalog GitHub repo immediately after the monorepo merge — wait until G5 is re-verified in a network-only scenario (no local clone). This is a post-SG4 housekeeping step, not part of this plan.

8. **Timing of catalog PR #9 merge.** If catalog PR #9 (`feat/category-backfill`) is merged to catalog `main` *after* the subtree add in §2.3, those commits are not included in the squash. They will be picked up on the first `sync-upstream.sh` (which re-fetches catalog — no, wrong: `sync-upstream.sh` fetches `upstream-skills`, not the catalog repo). The correct fix: ensure catalog PR #9 is merged **before** running `git subtree add` in §2.3. This is enforced by §1.1.

---

## 7. Sequence summary

```
§1.1 Merge PRs (forge #18, #19, #20, #21 + catalog #9 — independent, any order)
     ↓
§1.2 Rehearsal in throwaway clones (proves exact commands)
     ↓
§2   The merge (git subtree add --prefix=catalog)     [IRREVERSIBLE from §2.3]
     ↓
§3   Fix-ups branch: registry.go, sync-upstream.sh,
     upstream-changelog.py, catalog.yml              [PR; reversible until merge]
     ↓
§4   Verification gate G1–G9 + G5-b + G-sync
     ↓
     Cleanup: git remote remove catalog-source
              optional: archive standalone catalog GitHub repo
```

Total estimated session time: 2–3 hours (dominated by PR merges + rehearsal).

---

## 8. Provenance

Authored by `cs-senior-engineer` (2026-06-02). Based on read-only exploration of:
- `forge/internal/catalog/registry.go` (defaultRegistry, LoadRegistry, migrateSourceIDs from PR #20 branch)
- `forge/.github/workflows/ci.yml`, `release.yml`, `.goreleaser.yaml`, `Makefile`
- `claude-skills-jesper/scripts/sync-upstream.sh`, `regenerate-marketplace.py`, `upstream-changelog.py`, `check-sources.py`
- `claude-skills-jesper/skills/_shared/install-refresh-daemons.sh`
- forge open PRs #18, #19, #20, #21; catalog open PR #9
- `PLAN-forge-unification.md` (SG4 scope and verification gate)
