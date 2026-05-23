#!/usr/bin/env bash
# Fetch NVIDIA's docs catalog (llms.txt) and save a dated copy as the
# nvidia-dgx-research skill's reference.

set -euo pipefail

DIR="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$DIR/references/nvidia-catalog.md"
URL="https://docs.nvidia.com/llms.txt"

mkdir -p "$(dirname "$OUT")"

TMP="$(mktemp)"
trap 'rm -f "$TMP"' EXIT

curl -fsSL "$URL" > "$TMP"

if [[ ! -s "$TMP" ]]; then
  echo "ERROR: empty response from $URL" >&2
  exit 1
fi

DATE="$(date -u +"%Y-%m-%d %H:%M:%S UTC")"
PRODUCTS="$(grep -c "^## " "$TMP" || true)"

{
  echo "<!-- Generated: $DATE -->"
  echo "<!-- Source: $URL -->"
  echo "<!-- Products: $PRODUCTS -->"
  echo ""
  cat "$TMP"
} > "$OUT"

LINES="$(wc -l < "$OUT" | tr -d ' ')"
echo "Updated $OUT — $LINES lines, $PRODUCTS products"
