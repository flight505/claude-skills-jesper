# OpenRouter API Quick Reference

**Base URL:** https://openrouter.ai/api/v1

**Version:** Latest from OpenAPI specification

## Authentication

Include your API key in the Authorization header:
```
Authorization: Bearer YOUR_API_KEY
```

## API Endpoints

### POST /chat/completions
Create a chat completion

**Example:**
```bash
curl https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "anthropic/claude-sonnet-4-5",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

### GET /models
List all available models

**Example:**
```bash
curl https://openrouter.ai/api/v1/models \
  -H "Authorization: Bearer $OPENROUTER_API_KEY"
```

## Common Parameters

### Chat Completions

- **model** (required): Model ID (e.g., "anthropic/claude-sonnet-4-5")
- **messages** (required): Array of message objects with role and content
- **stream** (optional): Enable streaming responses (true/false)
- **max_tokens** (optional): Maximum tokens to generate
- **temperature** (optional): Randomness (0-2)
- **top_p** (optional): Nucleus sampling
- **presence_penalty** (optional): Penalize repeated tokens
- **frequency_penalty** (optional): Penalize token frequency

## Streaming

Enable streaming by setting `"stream": true`:

```bash
curl https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "anthropic/claude-sonnet-4-5",
    "messages": [{"role": "user", "content": "Hello!"}],
    "stream": true
  }'
```

## Response Format

Successful response:
```json
{
  "id": "gen-...",
  "model": "anthropic/claude-sonnet-4-5",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "Hello! How can I help you?"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 8,
    "total_tokens": 18
  }
}
```

## Error Codes

- **400**: Bad Request - Invalid parameters
- **401**: Unauthorized - Invalid API key
- **402**: Payment Required - Insufficient credits
- **429**: Too Many Requests - Rate limit exceeded
- **500**: Internal Server Error - OpenRouter issue

## Best Practices

1. Always include Authorization header
2. Handle rate limits with exponential backoff
3. Use streaming for long responses
4. Monitor your usage via dashboard
5. Set reasonable max_tokens to control costs

## Links

- Dashboard: https://openrouter.ai
- Documentation: https://openrouter.ai/docs
- API Keys: https://openrouter.ai/keys
- Models: https://openrouter.ai/models
