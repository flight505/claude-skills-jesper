# Extended Thinking

Deep reasoning mode for complex problems.

## When to Use Extended Thinking

- Multi-step mathematical reasoning
- Complex code analysis or debugging
- Strategic planning with many factors
- Problems requiring careful consideration of edge cases
- Tasks where showing reasoning improves trust

## When NOT to Use

- Simple factual queries
- Latency-sensitive applications
- Straightforward text generation
- Tasks where reasoning doesn't add value

## Configuration

### Basic Setup
```python
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=16000,
    thinking={
        "type": "enabled",
        "budget_tokens": 10000  # tokens allocated for thinking
    },
    messages=[...]
)
```

### Key Parameters

| Parameter | Description | Notes |
|-----------|-------------|-------|
| `budget_tokens` | Max tokens for thinking | Min 1024, affects cost |
| `type` | `"enabled"` or `"disabled"` | Cannot be changed mid-conversation |

## Response Structure

Extended thinking responses have two content block types:

```python
for block in response.content:
    if block.type == "thinking":
        print("Reasoning:", block.thinking)
    elif block.type == "text":
        print("Answer:", block.text)
```

## Streaming Extended Thinking

```python
with client.messages.stream(
    ...,
    thinking={"type": "enabled", "budget_tokens": 10000}
) as stream:
    for event in stream:
        if event.type == "content_block_start":
            if event.content_block.type == "thinking":
                print("Starting to think...")
        elif event.type == "content_block_delta":
            if hasattr(event.delta, "thinking"):
                print(event.delta.thinking, end="")
            elif hasattr(event.delta, "text"):
                print(event.delta.text, end="")
```

## Multi-Turn Conversations

**Critical:** Preserve thinking blocks when continuing conversations.

```python
# First turn
response1 = client.messages.create(
    thinking={"type": "enabled", "budget_tokens": 10000},
    messages=[{"role": "user", "content": "Complex question..."}]
)

# Second turn - include ALL previous content including thinking
messages = [
    {"role": "user", "content": "Complex question..."},
    {"role": "assistant", "content": response1.content},  # Includes thinking blocks!
    {"role": "user", "content": "Follow-up question..."}
]
response2 = client.messages.create(
    thinking={"type": "enabled", "budget_tokens": 10000},
    messages=messages
)
```

**Warning:** Stripping thinking blocks from conversation history degrades performance.

→ Source: `extended_thinking/` directory

## Budget Optimization

| Task Type | Suggested Budget |
|-----------|------------------|
| Simple reasoning | 2,000 - 5,000 |
| Moderate complexity | 5,000 - 10,000 |
| Complex analysis | 10,000 - 20,000 |
| Deep research | 20,000+ |

**Tip:** Start lower, increase if responses seem rushed or incomplete.

## Prompting for Extended Thinking

Good prompts for extended thinking:
- "Think through this step by step"
- "Consider all the edge cases"
- "Analyze the tradeoffs before recommending"

Avoid:
- "Quick answer please"
- "Just give me the result"

## Cost Considerations

- Thinking tokens count toward input costs
- Budget sets ceiling, actual usage may be lower
- Monitor `usage.thinking_tokens` in response
- Consider caching for repeated complex queries

## Limitations

- Cannot be enabled/disabled mid-conversation
- Thinking content visible to user (no hidden reasoning)
- Higher latency than standard responses
- Not available on all models - check model card
