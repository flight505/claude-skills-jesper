---
name: spark-docs-skill
category: productivity
description: USE THIS SKILL for any question about NVIDIA DGX Spark hardware, DGX OS 7, system setup, first boot, recovery, dashboard, NGC, containers, or DGX-specific software. This skill has complete local documentation — do not use web search or WebFetch instead.
pairs_with: nvidia-dgx-research
---

# NVIDIA DGX Spark Documentation Skill

**Intelligent documentation access for the NVIDIA DGX Spark (GB10) and DGX OS 7.**

## Path Resolution

Use `${CLAUDE_SKILL_DIR}` to reference this skill's directory — it resolves automatically whether the skill is symlinked or local.

## Overview

This skill bundles official NVIDIA documentation for two tightly coupled products:

- **DGX Spark** — the GB10 desktop / workstation system (hardware, software stack, dashboard, recovery, common use cases)
- **DGX OS 7** — the Ubuntu-based operating system that ships on Spark (installation, networking, storage, additional software)

Sources are Sphinx-generated documentation trees on `docs.nvidia.com`, fetched and indexed for local lookup. No `llms.txt` exists for these products, so the skill maintains its own snapshot.

## Documentation Update Requests

When user requests to update documentation (trigger: "update spark docs" / "update dgx documentation"):

```bash
"${CLAUDE_SKILL_DIR}/scripts/update-docs.sh"
```

**What gets updated:**
1. **Quick Reference** — Tier 1 — key pages: overview, first boot, hardware, common use cases, known issues
2. **Section Index** — Tier 2 — every page organized by `dgx-spark` vs `dgx-os-7-user-guide`
3. **Full Documentation** — Tier 3 — complete content with grep-friendly page markers

**Duration:** ~30 seconds (≈ 50 small pages with rate limiting)

**Error Handling:**
- Each page fetch status is logged
- Failed pages are skipped with warnings
- Aborts if <10 pages fetched (critical failure)

## 3-Tier Routing

### Tier 1: Quick Reference

- **File:** `references/quick-reference.md`
- **Covers:** System overview, first-boot setup, hardware spec, software stack, common use cases, known issues, DGX OS 7 entrypoint
- **Use when:** Initial Spark setup, hardware questions, "what is X on Spark?"

**Example queries:**
- "What hardware is in DGX Spark?"
- "How do I first-boot a DGX Spark?"
- "What common use cases does NVIDIA highlight for Spark?"
- "What are the known issues on DGX Spark right now?"

### Tier 2: Section Index

- **File:** `references/section-index.md`
- **Covers:** Every page in both doc trees, with title and short description
- **Use when:** Locating a specific topic, scoping which pages cover an area

**Example queries:**
- "Where is recovery documented for DGX Spark?"
- "What does the DGX OS 7 guide cover under additional software?"
- "List all pages in the DGX Spark section"

**Access pattern:**
```bash
grep -A 30 "^## DGX-SPARK"        references/section-index.md
grep -A 30 "^## DGX-OS-7-USER-GUIDE" references/section-index.md
grep -i "recovery"                 references/section-index.md
```

### Tier 3: Full Documentation

- **File:** `references/full-docs.txt`
- **Covers:** Complete prose for every page with grep markers
- **Use when:** Detailed instructions, exact command names, troubleshooting deep dives

**IMPORTANT:** Never load the entire file. Use grep markers for targeted extraction.

**Access patterns:**
```bash
# Find and extract a specific page
grep -A 200 "^PAGE: /dgx-spark/first-boot.html" references/full-docs.txt

# Find all pages in a section
grep "^PAGE:" references/full-docs.txt | grep "/dgx-spark/"

# Search for a keyword across all docs
grep -n "nvidia-sync" references/full-docs.txt

# Extract complete page between separators
sed -n '/^PAGE: \/dgx-spark\/system-recovery.html/,/^═\{80\}$/p' references/full-docs.txt
```

## Companion Skill

For questions that fall outside the bundled documentation — community issues on the NVIDIA developer forum, recent posts on the NVIDIA developer blog, or adjacent product docs (CUDA, NeMo, Jetson, Brev, etc. via the `llms.txt` catalog at `docs.nvidia.com/llms.txt`) — use the `nvidia-dgx-research` skill.

This skill = **snapshot**. The companion = **live search**.

## Response Format

**Always cite tier and source:**
- "From Quick Reference: …"
- "From Section Index (DGX-OS-7-USER-GUIDE): …"
- "From Full Docs (/dgx-spark/first-boot.html): …"

**Provide context:**
- Mention which doc tree the answer comes from (Spark vs OS 7)
- Link to the official URL when relevant: `https://docs.nvidia.com/dgx/<path>`
- Note "known issues" page references if the topic is recent

## Best Practices

### DO
- Start with Tier 1 for overview / setup / hardware questions
- Use Tier 2 to find which page covers a specific topic
- Use targeted grep on Tier 3 for deep details (never load full file)
- Cite the page path in responses

### DON'T
- Load entire `full-docs.txt`
- Answer from training data — these are recent products, always check the local snapshot
- Use WebFetch / WebSearch for anything in scope of these docs
- Confuse DGX Spark (Grace Blackwell desktop) with the larger DGX servers — they're different products

## File Locations

```
spark-docs-skill/
├── SKILL.md
├── docs-config.yaml
├── references/
│   ├── quick-reference.md
│   ├── section-index.md
│   └── full-docs.txt
└── scripts/
    └── update-docs.sh
```

## Maintenance

| Frequency | Reason |
|-----------|--------|
| Monthly | DGX docs change slowly — Sunday day 1 of the month via launchd |
| On request | When user asks about a feature missing from the snapshot |

**Manual refresh:**
```bash
"${CLAUDE_SKILL_DIR}/scripts/update-docs.sh"
```

**Automated refresh:** `~/Library/LaunchAgents/com.flight505.spark-docs-refresh.plist`

## Version

**Skill Version:** 1.0.0
**Documentation Sources:**
- https://docs.nvidia.com/dgx/dgx-spark/
- https://docs.nvidia.com/dgx/dgx-os-7-user-guide/

---

**Remember:** Tier 1 first → Tier 2 to find topics → Tier 3 for deep details. For forum/blog/adjacent-product questions, hand off to `nvidia-dgx-research`.
