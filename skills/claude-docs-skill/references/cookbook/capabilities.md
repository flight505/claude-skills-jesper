# Capabilities

Patterns for classification, summarization, RAG, and text-to-SQL.

## Classification

Use Claude for text categorization with high accuracy.

### When to Use
- Sentiment analysis
- Intent detection
- Content moderation
- Topic categorization
- Support ticket routing

### Approaches

**Direct Classification:**
```
Classify the following text into one of: [categories]
Text: {input}
Category:
```

**Structured Output (more reliable):**
Use tool calling to force structured classification response with confidence scores.

**Few-Shot Classification:**
Provide examples for each category to improve accuracy on domain-specific tasks.

→ Source: `capabilities/classification/guide.ipynb`

### Best Practices
- Provide clear category definitions
- Include edge case examples
- Consider hierarchical classification for complex taxonomies
- Use confidence thresholds for human review escalation

## Summarization

Condense long documents while preserving key information.

### When to Use
- Document summarization
- Meeting notes
- Research paper abstracts
- News article digests

### Approaches

**Extractive:** Pull key sentences verbatim
**Abstractive:** Generate new summary text (Claude's default)
**Hierarchical:** Summarize sections, then summarize summaries (for very long docs)

### Techniques

**Length Control:**
```
Summarize in exactly 3 bullet points / 100 words / one paragraph
```

**Focus Control:**
```
Summarize focusing on: financial implications / technical details / action items
```

**Audience Adaptation:**
```
Summarize for: executives / technical team / general audience
```

→ Source: `capabilities/summarization/guide.ipynb`

## Retrieval Augmented Generation (RAG)

Ground Claude's responses in your data.

### When to Use
- Question answering over documents
- Knowledge base queries
- Up-to-date information retrieval
- Domain-specific expertise

### Architecture

```
Query → Embed → Vector Search → Top-K Chunks → Claude + Context → Answer
```

### Key Components

1. **Chunking:** Split documents into retrievable units (512-1024 tokens typical)
2. **Embedding:** Convert chunks to vectors (VoyageAI, OpenAI, etc.)
3. **Retrieval:** Find relevant chunks via similarity search
4. **Generation:** Claude synthesizes answer from retrieved context

### Best Practices

- **Chunk overlap:** 10-20% overlap prevents losing context at boundaries
- **Metadata:** Store source, date, section for filtering and citations
- **Reranking:** Use a reranker to improve retrieval precision
- **Context window:** Don't overstuff - 5-10 highly relevant chunks often beats 50 mediocre ones

→ Source: `capabilities/retrieval_augmented_generation/`

### Contextual Embeddings
Enhance chunk embeddings with surrounding context for better retrieval.

→ Source: `capabilities/contextual-embeddings/`

## Text-to-SQL

Generate SQL queries from natural language.

### When to Use
- Natural language database interfaces
- Business intelligence queries
- Data exploration tools

### Approach

1. **Schema in context:** Provide table definitions, column descriptions, relationships
2. **Examples:** Include sample queries for your specific schema
3. **Validation:** Parse and validate generated SQL before execution
4. **Iteration:** If query fails, send error back for correction

### Schema Representation
```sql
-- Users table: stores customer information
-- Columns: id (PK), name, email, created_at, plan_type (free|pro|enterprise)
CREATE TABLE users (...)
```

### Safety
- Use read-only database connections
- Validate queries against allowlist of operations
- Set query timeouts
- Never expose raw errors to end users

→ Source: `capabilities/text_to_sql/`

## Evaluation

Build robust evals to measure capability performance.

### Components

1. **Test cases:** Input/expected output pairs
2. **Metrics:** Accuracy, F1, BLEU, custom rubrics
3. **Baselines:** Compare against simple heuristics
4. **Error analysis:** Categorize failure modes

→ Source: `misc/building_evals.ipynb`, `misc/generate_test_cases.ipynb`
