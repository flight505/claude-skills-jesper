# Advanced Patterns

Skills, document generation, frontend aesthetics, and finetuning.

## Skills (Beta)

Skills enable Claude to create professional documents (Excel, PowerPoint, PDF, Word).

### When to Use
- Generating formatted business documents
- Creating data visualizations in Excel
- Building presentation decks
- Producing print-ready PDFs

### Available Skills
| Skill | Output | Use For |
|-------|--------|---------|
| `xlsx` | Excel workbooks | Data analysis, charts, pivot tables, financial models |
| `pptx` | PowerPoint | Presentations, pitch decks, slide reports |
| `pdf` | PDF documents | Formal reports, print documents |
| `docx` | Word documents | Reports, memos, long-form content |

### Implementation
```python
response = client.beta.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=4096,
    betas=["code-execution-2025-08-25", "files-api-2025-04-14", "skills-2025-10-02"],
    messages=[...],
    container={"type": "skill", "name": "xlsx"}
)

# Download generated file
for block in response.content:
    if block.type == "file":
        file_content = client.beta.files.download(block.file_id)
```

**Note:** Generation takes ~1-2 minutes. Files stored temporarily on Anthropic servers.

→ Source: `skills/notebooks/`

## Custom Skills

Extend Claude with domain-specific expertise.

### Architecture
```
skill/
├── SKILL.md          # Instructions and prompts
├── scripts/          # Executable code
└── resources/        # Templates, data files
```

### Examples
- **Financial Modeling:** DCF analysis, Monte Carlo simulations
- **Brand Guidelines:** Apply corporate styling to documents
- **Domain Calculators:** Industry-specific computations

→ Source: `skills/custom_skills/`

## Frontend Aesthetics

Improve Claude's UI/UX code generation quality.

### The Problem
Claude tends toward "AI slop" - generic, bland interfaces (Inter font, gray colors, basic layouts).

### Solutions

**Typography:**
- Specify distinctive fonts: JetBrains Mono, Playfair Display, Clash Display
- Avoid: Inter, Roboto, Arial (overused defaults)

**Color & Theme:**
- Reference specific themes: Solarpunk, Nord, Dracula, Catppuccin
- Use CSS variables for consistency
- Draw from IDE themes and cultural aesthetics

**Motion:**
- CSS-only for HTML artifacts
- Focus on high-impact moments
- Staggered reveals, meaningful transitions

**Backgrounds:**
- Avoid solid colors
- Use gradients, subtle patterns, contextual effects

### Prompting Techniques
```
# Bad
"Create a dashboard"

# Better
"Create a dashboard with:
- Typography: JetBrains Mono for data, Space Grotesk for headings
- Theme: Dark mode inspired by GitHub's interface
- Subtle gradient backgrounds, not flat colors
- Avoid generic gray - use deep blues and teals"
```

→ Source: `coding/prompting_for_frontend_aesthetics.ipynb`

## Finetuning

Adapt Claude to specific domains via supervised finetuning.

### When to Consider
- Consistent specialized output format required
- Domain-specific knowledge/terminology
- Behavioral customization (tone, style)
- Cost optimization (smaller finetuned model)

### Process (AWS Bedrock)
1. Prepare JSONL dataset with conversation examples
2. Upload to S3
3. Launch finetuning job via Bedrock
4. Deploy via Provisioned Throughput

### Dataset Format
```jsonl
{"system": "optional", "messages": [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]}
```

**Requirements:**
- First message must be `user`
- Last message must be `assistant`
- Minimum 2 messages per example

→ Source: `finetuning/finetuning_on_bedrock.ipynb`

### Alternatives to Finetuning
Consider before finetuning:
1. Better prompting (cheaper, faster iteration)
2. Few-shot examples (no training needed)
3. RAG for knowledge (more maintainable)

Finetune when: prompting plateau reached, consistent format critical, high volume justifies cost.

## Moderation Filter

Build content moderation using Claude.

### Pattern
```python
def moderate(content):
    response = client.messages.create(
        model="claude-haiku-...",  # Fast, cheap
        messages=[{
            "role": "user",
            "content": f"Classify if harmful: {content}"
        }],
        tools=[{
            "name": "classify",
            "input_schema": {
                "properties": {
                    "is_harmful": {"type": "boolean"},
                    "category": {"enum": ["safe", "hate", "violence", ...]},
                    "confidence": {"type": "number"}
                }
            }
        }],
        tool_choice={"type": "tool", "name": "classify"}
    )
    return parse_tool_call(response)
```

**Best practices:**
- Use Haiku for speed and cost
- Define clear category taxonomy
- Set confidence thresholds for human review
- Log edge cases for evaluation improvement

→ Source: `misc/building_moderation_filter.ipynb`

## Metaprompt

Generate optimized prompts using Claude.

### Use For
- Creating task-specific system prompts
- Iterating on prompt quality
- Prompt engineering automation

→ Source: `misc/metaprompt.ipynb`
