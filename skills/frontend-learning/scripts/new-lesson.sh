#!/usr/bin/env bash
# new-lesson.sh — scaffold a blank lesson file
# Usage: ./scripts/new-lesson.sh "Attention Mechanism"
#
# This creates lessons/YYYY-MM-DD-<slug>.html containing the html-template.md
# starter with the title pre-filled. Claude then fills in the body.

set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 \"Lesson title\""
  exit 1
fi

title="$1"
slug=$(echo "$title" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g; s/^-|-$//g')
date_prefix=$(date +%Y-%m-%d)

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
project_root="$(dirname "$script_dir")"
lessons_dir="$project_root/lessons"
mkdir -p "$lessons_dir"

out="$lessons_dir/${date_prefix}-${slug}.html"

if [[ -f "$out" ]]; then
  echo "Already exists: $out"
  exit 1
fi

# Print the target path so Claude (or the user) knows where to write.
# We don't pre-fill the template here — Claude reads html-template.md and
# writes the file directly so the body can be authored in one pass.
echo "$out"
