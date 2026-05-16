# Third-Party Integrations

Patterns for integrating Claude with external services and tools.

## Vector Databases

### Pinecone
Managed vector database for semantic search.

**Use for:** Production RAG, scalable similarity search

**Pattern:**
1. Embed documents with embedding model
2. Upsert to Pinecone index
3. Query with embedded user question
4. Pass top-K results to Claude

→ Source: `third_party/Pinecone/`

### MongoDB Atlas Vector Search
Vector search within MongoDB ecosystem.

**Use for:** Existing MongoDB users, hybrid search (vector + filters)

**Pattern:** Similar to Pinecone but with MongoDB query syntax for filtering

→ Source: `third_party/MongoDB/`

## Embedding Providers

### Voyage AI
High-quality embeddings optimized for retrieval.

**Models:**
- `voyage-3` - General purpose
- `voyage-code-3` - Code-optimized
- `voyage-3-lite` - Faster, lower cost

**Use for:** RAG applications, semantic search, clustering

→ Source: `third_party/VoyageAI/`

## Orchestration Frameworks

### LlamaIndex
Framework for building RAG and agent applications.

**Features:**
- Document loaders for various formats
- Chunking strategies
- Index abstractions
- Query engines

**Use for:** Rapid RAG prototyping, complex document pipelines

→ Source: `third_party/LlamaIndex/`

## Audio/Voice

### Deepgram
Speech-to-text and text-to-speech.

**Use for:** Voice interfaces, transcription, audio analysis

**Pattern:**
1. Deepgram transcribes audio
2. Claude processes transcript
3. Optionally convert response to speech

→ Source: `third_party/Deepgram/`

### ElevenLabs
High-quality text-to-speech synthesis.

**Use for:** Voice assistants, audio content generation

→ Source: `third_party/ElevenLabs/`

## Knowledge Sources

### Wikipedia
Access to encyclopedic knowledge.

**Use for:** Fact-checking, background research, entity information

→ Source: `third_party/Wikipedia/`

### Wolfram Alpha
Computational knowledge engine.

**Use for:** Math calculations, scientific queries, factual lookups

→ Source: `third_party/WolframAlpha/`

## Integration Patterns

### Tool-Based Integration
Define external service as a tool Claude can call.

```python
tools=[{
    "name": "search_knowledge_base",
    "description": "Search internal docs for relevant information",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {"type": "string"}
        }
    }
}]
```

### Pre-Processing Integration
Process data before Claude sees it.

```
User Input → External API → Enriched Context → Claude → Response
```

### Post-Processing Integration
Use Claude's output to trigger external actions.

```
User Input → Claude → Structured Output → External API → Confirmation
```

## Best Practices

1. **Error handling:** External services fail - have fallbacks
2. **Caching:** Cache expensive external calls when appropriate
3. **Rate limiting:** Respect external API limits
4. **Timeouts:** Set reasonable timeouts for external calls
5. **Credentials:** Use environment variables, never hardcode
6. **Logging:** Track external calls for debugging and cost monitoring

## MCP (Model Context Protocol)

Standardized protocol for connecting Claude to external services.

**When to use MCP:**
- Building reusable integrations
- Need bidirectional communication
- Want standardized tool interfaces

**When to use direct API:**
- Simple one-off integrations
- Performance-critical paths
- Non-standard interaction patterns

→ See official docs: `agents-and-tools/mcp-connector`
