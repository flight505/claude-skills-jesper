#!/usr/bin/env bash
# Pull the latest alirezarezvani/claude-skills via git subtree and regenerate
# .claude-plugin/marketplace.json.
#
# Usage:
#   scripts/sync-upstream.sh            # pull main, then regenerate
#   scripts/sync-upstream.sh --dry-run  # show what a sync would change (no fetch, no regen)
#   scripts/sync-upstream.sh --ref TAG  # pull a specific ref instead of main
#
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

REMOTE_NAME="upstream-skills"
REMOTE_URL="https://github.com/alirezarezvani/claude-skills.git"
PREFIX="upstream"
REF="main"
DRY_RUN=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRY_RUN=1; shift;;
    --ref) REF="$2"; shift 2;;
    -h|--help) head -n 10 "$0" | tail -n 9; exit 0;;
    *) echo "unknown arg: $1" >&2; exit 2;;
  esac
done

# Only the upstream/ subtree must be clean for `git subtree pull` to apply.
# Unrelated in-progress first-party edits (skills/, scripts/, docs) should not
# block a sync — scope the dirty check to the subtree prefix.
if [[ -n "$(git status --porcelain -- upstream/)" ]]; then
  echo "error: upstream/ has uncommitted changes; commit or stash them before syncing." >&2
  git status --short -- upstream/ >&2
  exit 1
fi

if ! git remote get-url "$REMOTE_NAME" >/dev/null 2>&1; then
  echo "[setup] adding remote $REMOTE_NAME → $REMOTE_URL"
  git remote add "$REMOTE_NAME" "$REMOTE_URL"
fi

echo "[fetch] $REMOTE_NAME $REF"
git fetch "$REMOTE_NAME" "$REF" --quiet

if [[ $DRY_RUN -eq 1 ]]; then
  echo "[dry-run] preview of upstream changes:"
  python3 scripts/upstream-changelog.py --against "$REMOTE_NAME/$REF" || true
  exit 0
fi

# Show preview BEFORE pulling so a destructive subtree merge is informed
echo "[preview] changes that will land:"
python3 scripts/upstream-changelog.py --against "$REMOTE_NAME/$REF" || true
echo

echo "[subtree pull] $PREFIX ← $REMOTE_NAME/$REF (squash)"
git subtree pull --prefix="$PREFIX" "$REMOTE_NAME" "$REF" --squash \
  -m "chore: sync upstream alirezarezvani/claude-skills@$REF"

echo "[regenerate] marketplace.json"
python3 scripts/regenerate-marketplace.py --verbose

if [[ -n "$(git status --porcelain .claude-plugin/marketplace.json)" ]]; then
  git add .claude-plugin/marketplace.json
  git commit -q -m "chore: regenerate marketplace.json after upstream sync"
  echo "[commit] regenerated marketplace.json committed"
fi

echo "[done] upstream synced."
