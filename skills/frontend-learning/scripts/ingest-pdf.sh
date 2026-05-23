#!/usr/bin/env bash
# ingest-pdf.sh — parse a local PDF as clean markdown for use as lesson source material
#
# Like ingest-url.sh, this DOCUMENTS the workflow — actual parsing happens
# via the firecrawl-parse skill which handles PDFs, DOCX, etc. cleanly.
#
# Usage from inside Claude Code:
#   1. Invoke the firecrawl-parse skill on the PDF path
#   2. Optionally save the returned markdown to lessons/source/<slug>.md
#   3. Then architect the lesson from that source (see SKILL.md Phase 1)

cat <<'EOF'
PDF ingestion workflow:

  1. Use the firecrawl-parse skill on the target PDF path.
     The skill returns clean markdown, handles tables, math, and figures
     much better than pdftotext.

  2. For long papers, consider asking firecrawl-parse for an AI-generated
     summary too — useful for orienting before deep-reading.

  3. CRITICAL: don't translate the paper 1:1 into a lesson. ML papers are
     written for peers, not learners. The paper's "Method" section is rarely
     where the intuition lives. Look in "Introduction" for the puzzle, in
     "Related Work" for what was wrong before, in "Figure 1" for the central
     analogy, and in "Limitations" for the failure modes you must teach.

  4. Build the lesson via the normal Phase 1-4 workflow in SKILL.md.
EOF
