#!/usr/bin/env bash
# open-lesson.sh — open a lesson .html in the user's default browser
# Usage: ./scripts/open-lesson.sh lessons/2026-05-21-attention.html

set -euo pipefail

if [[ $# -lt 1 ]]; then
  # No arg → open the most recent lesson
  script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  project_root="$(dirname "$script_dir")"
  latest=$(ls -t "$project_root/lessons/"*.html 2>/dev/null | head -1)
  if [[ -z "$latest" ]]; then
    echo "No lessons found in $project_root/lessons/"
    exit 1
  fi
  target="$latest"
else
  target="$1"
fi

if [[ ! -f "$target" ]]; then
  echo "Not found: $target"
  exit 1
fi

case "$(uname -s)" in
  Darwin*) open "$target" ;;
  Linux*)  xdg-open "$target" ;;
  *)       echo "Open manually: $target" ;;
esac
