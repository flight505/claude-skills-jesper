---
name: nvidia-dgx-research
description: USE THIS SKILL for NVIDIA topics not covered by the local spark-docs-skill snapshot — community discussion on the NVIDIA developer forum, NVIDIA developer blog posts, and adjacent NVIDIA product docs (CUDA, NeMo, Jetson, Brev, Dynamo, and others listed in the docs.nvidia.com llms.txt catalog). This is a dispatcher skill that routes queries to WebSearch and WebFetch; it does NOT bundle bulk documentation.
pairs_with: spark-docs-skill
---

# NVIDIA DGX Research Skill

**Live search and structured docs lookup for NVIDIA topics outside the bundled DGX Spark / DGX OS 7 snapshot.**

## Path Resolution

Use `${CLAUDE_SKILL_DIR}` to reference this skill's directory.

## What this skill is for

This is the **companion** to `spark-docs-skill`. That skill bundles a local snapshot of DGX Spark and DGX OS 7 documentation. **This** skill handles everything else NVIDIA-related, on-demand:

1. **Adjacent NVIDIA products** (CUDA, NeMo, Jetson, Brev, Dynamo, Cosmos, …) — fetch the product's `llms.txt` or `llms-full.txt` from the catalog.
2. **NVIDIA developer forum** — community Q&A, real-world issues, fixes, threads about DGX Spark and surrounding ecosystem.
3. **NVIDIA developer blog** — official engineering posts, announcements, deep-dives.

## Routing Decision Tree

Use this order:

| Query is about | Route |
|---|---|
| DGX Spark hardware, DGX OS 7, first boot, dashboard, recovery, NGC, container runtime on Spark | **Hand off to `spark-docs-skill`** (it has the snapshot) |
| Another NVIDIA product with docs at `docs.nvidia.com/<product>` | **Mode 1: catalog fetch** |
| A bug, error, configuration question that sounds like community knowledge | **Mode 2: forum search** |
| A recent announcement, technique deep-dive, or "what is NVIDIA's stance on X" | **Mode 3: blog search** |

When in doubt: try Mode 1 first (cheapest and most authoritative), fall back to Mode 2 (community), then Mode 3 (blog).

## Mode 1: Catalog Fetch (adjacent NVIDIA products)

The local catalog at `references/nvidia-catalog.md` is a snapshot of `docs.nvidia.com/llms.txt`. It lists ~21 NVIDIA products, each with a `llms.txt` URL (curated index) and most with a `llms-full.txt` URL (entire docs in one file).

**Step 1:** grep the catalog for the product the user is asking about.
```bash
grep -B 1 -A 3 -i "cuda\|nemo\|jetson\|brev\|dynamo" "${CLAUDE_SKILL_DIR}/references/nvidia-catalog.md"
```

**Step 2:** WebFetch the product's `llms.txt` first (smaller, curated URL list with descriptions). Read it to identify the page that answers the question. Most product `llms.txt` files are 5–15KB.

**Step 3:** If a specific page URL is identified, WebFetch that page (or its `.md` sibling if NVIDIA hosts one).

**Step 4 (heavy queries only):** If the question is broad — "how do I do X in NeMo Curator?" — WebFetch the product's `llms-full.txt` instead. **Be aware:** these can be 1–10MB. Only do this for questions that genuinely require full corpus context.

**Example:**
- User: "How do I run a CUDA kernel from Python on Spark?"
- `grep -A 3 "CUDA" references/nvidia-catalog.md` → `https://docs.nvidia.com/cuda/llms.txt`
- WebFetch that, scan for "Python", follow the specific section URL.

## Mode 2: Forum Search (community knowledge)

NVIDIA developer forum, DGX Spark category and the broader accelerated-computing tags.

**Tool:** built-in `WebSearch` with site filter.

**Query shape:**
```
<the user's question> site:forums.developer.nvidia.com
```

**Targeted to DGX Spark specifically:**
```
<question> site:forums.developer.nvidia.com/c/accelerated-computing/dgx-spark-gb10
```

**When to use:**
- "Anyone else seeing X?"
- "Is there a known workaround for Y?"
- "What did NVIDIA staff say about Z?"
- Errors / stack traces / specific symptoms

**After search:** the top result is usually a forum thread. WebFetch it to read full discussion (forum threads are paywall-free).

## Mode 3: Blog Search (official NVIDIA posts)

NVIDIA developer blog publishes engineering deep-dives, model releases, GTC recap content, etc.

**Tool:** built-in `WebSearch` with site filter.

**Query shape:**
```
<topic> site:developer.nvidia.com/blog
```

**When to use:**
- "What's NVIDIA's recent guidance on X?"
- "Has NVIDIA published anything about Y?"
- "Summarize NVIDIA's announcement around Z"

**After search:** WebFetch the top result for full content if needed.

## Anti-Patterns

**Don't** use this skill for:
- DGX Spark hardware / OS 7 / dashboard / first-boot questions → use `spark-docs-skill`
- Plain "what is GPU memory" / general CUDA basics → that's in Claude's training data, no skill needed
- Searching for `llms-full.txt` corpora when a small `llms.txt` would do — costs nothing but bandwidth
- Synthesis-heavy "compare X across NVIDIA's whole product line" — that needs Perplexity-style search, beyond this skill's scope

## Files

```
nvidia-dgx-research/
├── SKILL.md
├── references/
│   └── nvidia-catalog.md     # Snapshot of docs.nvidia.com/llms.txt (~5KB, 21 products)
└── scripts/
    └── update-catalog.sh     # Refresh the catalog snapshot
```

## Maintenance

| Frequency | Reason |
|-----------|--------|
| Monthly | NVIDIA adds new products to the catalog occasionally — first Sunday of the month via launchd |
| On request | If a query expects a product that isn't in the local catalog |

**Manual refresh:**
```bash
"${CLAUDE_SKILL_DIR}/scripts/update-catalog.sh"
```

**Automated refresh:** `~/Library/LaunchAgents/com.flight505.nvidia-dgx-research-refresh.plist`

## Version

**Skill Version:** 1.0.0
**Catalog Source:** https://docs.nvidia.com/llms.txt
**Companion Skill:** `spark-docs-skill` (DGX Spark + DGX OS 7 snapshot)

---

**Remember:** Adjacent NVIDIA product → Mode 1 (catalog). Community issue → Mode 2 (forum search). Official announcement / deep-dive → Mode 3 (blog search). DGX Spark itself → hand off to `spark-docs-skill`.
