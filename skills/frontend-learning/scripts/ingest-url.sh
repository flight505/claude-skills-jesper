#!/usr/bin/env bash
# ingest-url.sh — fetch a URL as clean markdown for use as lesson source material
#
# This script intentionally just DOCUMENTS the workflow — the actual ingestion
# happens via the firecrawl-scrape skill in Claude Code, not via curl/wget.
# firecrawl-scrape handles JS-rendered SPAs, returns LLM-optimized markdown,
# and respects rate limits.
#
# Usage from inside Claude Code:
#   1. Invoke the firecrawl-scrape skill on the URL
#   2. Save the returned markdown to lessons/source/<slug>.md
#   3. Then architect the lesson from that source (see SKILL.md Phase 1)
#
# This script exists mostly as a workflow reminder.

cat <<'EOF'
URL ingestion workflow:

  1. Use the firecrawl-scrape skill on the target URL.
     The skill returns clean LLM-optimized markdown, handles JS-rendered SPAs,
     and works much better than curl | sed for content extraction.

  2. Don't write the markdown to disk unless you want to keep it as a source
     artifact alongside the lesson. Most of the time, read it directly into
     context, architect the lesson, then discard.

  3. CRITICAL: don't translate the source 1:1 into a lesson. The source's
     section headings are NOT your section headings. Find the central
     misconception, the motivating puzzle, and the wrong intuitions — build
     the lesson from THOSE. See SKILL.md, "Ingestion".

  4. Build the lesson via the normal Phase 1-4 workflow in SKILL.md.
EOF
