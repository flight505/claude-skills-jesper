# API Patterns

Essential patterns for working with the Claude API efficiently.

## Prompt Caching

Reduce costs and latency by caching static prompt content.

### When to Use
- Long system prompts reused across requests
- Few-shot examples that don't change
- Large document context referenced repeatedly

### Implementation
```python
# Mark content for caching with cache_control
messages=[{
    "role": "user",
    "content": [
        {
            "type": "text",
            "text": "<large static context>",
            "cache_control": {"type": "ephemeral"}
        },
        {
            "type": "text",
            "text": "User's actual question"
        }
    ]
}]
```

**Key points:**
- Cache has 5-minute TTL (refreshed on use)
- Minimum 1024 tokens to cache (2048 for Claude 3.5)
- Cached content must be at start of prompt
- Monitor `cache_creation_input_tokens` and `cache_read_input_tokens` in response

→ Source: `misc/prompt_caching.ipynb`

### Speculative Caching
For dynamic prompts, cache the static prefix and vary the suffix.

→ Source: `misc/speculative_prompt_caching.ipynb`

## Batch Processing

Process large volumes at 50% cost reduction with 24-hour turnaround.

### When to Use
- Non-time-sensitive bulk processing
- Evaluation runs
- Data transformation pipelines

### Implementation
```python
# Create batch with JSONL file
batch = client.messages.batches.create(
    requests=[
        {"custom_id": "req-1", "params": {...}},
        {"custom_id": "req-2", "params": {...}},
    ]
)

# Poll for completion
batch = client.messages.batches.retrieve(batch.id)
# status: "in_progress" | "ended"

# Retrieve results
for result in client.messages.batches.results(batch.id):
    print(result.custom_id, result.result)
```

→ Source: `misc/batch_processing.ipynb`

## JSON Mode / Structured Outputs

Force valid JSON responses.

### Tool-Based Extraction
Define a tool with your desired schema - Claude will call it with structured data.

```python
tools=[{
    "name": "extract_data",
    "description": "Extract structured data",
    "input_schema": {
        "type": "object",
        "properties": {...},
        "required": [...]
    }
}],
tool_choice={"type": "tool", "name": "extract_data"}
```

→ Source: `misc/how_to_enable_json_mode.ipynb`

## Citations

Track source attribution in responses.

### When to Use
- RAG applications requiring source links
- Document Q&A with provenance
- Fact-checking workflows

### Implementation
Enable citations and provide source documents:

```python
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    messages=[...],
    citations={"enabled": True}
)
# Response includes citation markers linked to source spans
```

→ Source: `misc/using_citations.ipynb`

## Streaming

Get partial responses as they generate.

### When to Use
- Interactive applications (chatbots, real-time UI)
- Long responses where user shouldn't wait
- Progress indication for complex tasks

### Implementation
```python
with client.messages.stream(...) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

**Event types:** `message_start`, `content_block_start`, `content_block_delta`, `message_stop`

## Token Counting

Estimate costs before sending requests.

```python
count = client.messages.count_tokens(
    model="claude-sonnet-4-20250514",
    messages=[...],
    system="...",
    tools=[...]
)
print(count.input_tokens)
```

→ Source: `misc/sampling_past_max_tokens.ipynb`

## Handling Long Outputs

When response may exceed `max_tokens`:

1. Set `max_tokens` generously
2. Check `stop_reason` - if `"max_tokens"`, response was truncated
3. Continue generation by appending assistant message and requesting more

→ Source: `misc/sampling_past_max_tokens.ipynb`

## Error Handling Best Practices

| Error | Retry? | Action |
|-------|--------|--------|
| 400 Bad Request | No | Fix request format |
| 401 Unauthorized | No | Check API key |
| 429 Rate Limited | Yes | Exponential backoff |
| 500 Server Error | Yes | Retry with backoff |
| 529 Overloaded | Yes | Retry with longer backoff |

**Recommended:** Use SDK's built-in retry logic or implement exponential backoff with jitter.
