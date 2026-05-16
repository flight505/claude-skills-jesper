# Tool Use Patterns

Quick reference for Claude API tool calling patterns and techniques.

## When to Use Tool Calling

- Extracting structured data from unstructured input
- Connecting Claude to external APIs, databases, or services
- Building multi-step workflows requiring real-world actions
- Forcing specific output formats (JSON extraction via tools)

## Core Patterns

### Basic Tool Calling
Single tool definition, single invocation per turn. Best for simple extractions or lookups.

**Key parameters:**
```python
tools=[{"name": "...", "description": "...", "input_schema": {...}}]
```

→ Source: `tool_use/calculator_tool.ipynb`

### Parallel Tool Calling
Multiple tools invoked in a single response. Use when actions are independent and can execute concurrently.

→ Source: `tool_use/parallel_tools.ipynb`

### Tool Choice Control
Force or restrict tool usage mid-conversation:

| Setting | Behavior |
|---------|----------|
| `{"type": "auto"}` | Claude decides (default) |
| `{"type": "any"}` | Must use at least one tool |
| `{"type": "tool", "name": "X"}` | Must use specific tool |
| `{"type": "none"}` | Disable tools for this turn |

→ Source: `tool_use/tool_choice.ipynb`

### Structured JSON Extraction
Use tool definitions to force structured output even without executing tools. Define a "extraction" tool with desired schema.

→ Source: `tool_use/extracting_structured_json.ipynb`

## Advanced Patterns

### Vision + Tools
Combine image analysis with tool calling. Send images in content blocks alongside tool definitions.

→ Source: `tool_use/vision_with_tools.ipynb`

### Tool Search with Embeddings
For large tool sets (50+), use embeddings to find relevant tools dynamically rather than sending all definitions.

**When to use:** Tool count exceeds context efficiency, tools are domain-specific

→ Source: `tool_use/tool_search_with_embeddings.ipynb`

### Programmatic Tool Calling (PTC)
Let Claude generate structured tool calls that execute in your environment without API round-trips. Reduces latency for simple tool chains.

→ Source: `tool_use/programmatic_tool_calling_ptc.ipynb`

### Memory Tool Pattern
Persistent context across conversations using a memory tool that stores/retrieves key information.

→ Source: `tool_use/memory_cookbook.ipynb`

### Automatic Context Compaction
Manage long conversations by compacting history when approaching token limits.

→ Source: `tool_use/automatic-context-compaction.ipynb`

## Tool Schema Best Practices

1. **Descriptions matter** - Claude uses descriptions to decide when/how to use tools
2. **Required vs optional** - Mark truly required fields; optional fields reduce call failures
3. **Enums for constraints** - Use enums when values must be from a fixed set
4. **Examples in descriptions** - Add example values for complex parameters

## Common Pitfalls

- Forgetting to handle `tool_use` stop reason and send back `tool_result`
- Overly vague tool descriptions leading to misuse
- Not validating tool inputs before execution
- Sending too many tools (context bloat) - consider tool search for 20+ tools
