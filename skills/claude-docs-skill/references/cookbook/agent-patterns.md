# Agent Patterns

Reference implementations for agentic workflows based on Anthropic's "Building Effective Agents" research.

## When to Use Agents

- Tasks requiring multiple reasoning steps with external actions
- Complex research or analysis spanning multiple sources
- Workflows needing plan → execute → evaluate cycles
- Tasks where quality matters more than latency

## Basic Building Blocks

### Prompt Chaining
Sequential LLM calls where output becomes input for next step.

**Use for:** Multi-step analysis, document processing pipelines, sequential reasoning

**Pattern:**
```
Input → LLM₁ → Output₁ → LLM₂ → Output₂ → Final
```

→ Source: `patterns/agents/basic_workflows.ipynb`

### Routing
Classify input to direct to specialized prompts or handlers.

**Use for:** Customer support triage, content moderation, task classification

**Pattern:**
```
Input → Classifier → Route A (specialized prompt)
                  → Route B (different prompt)
                  → Route C (escalate/reject)
```

→ Source: `patterns/agents/basic_workflows.ipynb`

### Parallelization
Process multiple inputs concurrently with same prompt template.

**Use for:** Batch processing, exploring multiple approaches, concurrent analysis

**Implementation:** `ThreadPoolExecutor` for parallel API calls

→ Source: `patterns/agents/basic_workflows.ipynb`

## Advanced Workflows

### Orchestrator-Subagents
Central coordinator delegates specialized tasks to parallel subagents, then aggregates findings.

**Components:**
- **Research Lead** - Plans strategy, breaks down questions, determines query types
- **Research Subagents** - Execute focused research tasks in parallel
- **Aggregator** - Synthesizes findings into coherent output

**Query Types:**
- Depth-first: Deep dive on single topic
- Breadth-first: Survey across multiple sources
- Straightforward: Direct factual lookup

→ Source: `patterns/agents/orchestrator_workers.ipynb`

### Evaluator-Optimizer Loop
Iterative refinement where evaluator assesses quality and sends back for improvement.

**Pattern:**
```
Input → Generator → Output → Evaluator → [Pass] → Final
                                      → [Fail] → Generator (with feedback)
```

**Use for:** Quality assurance, iterative content refinement, complex generation

→ Source: `patterns/agents/evaluator_optimizer.ipynb`

## Agent SDK Patterns

The Claude Agent SDK provides higher-level abstractions for building agents.

### Basic Agent
Single agent with tools and instructions.

**Key concepts:**
- `Agent` class with model, instructions, tools
- `Runner` to execute agent turns
- Automatic tool result handling

→ Source: `claude_agent_sdk/research_agent/`

### Multi-Agent Systems
Multiple specialized agents coordinating on complex tasks.

**Chief of Staff Pattern:**
- Coordinator agent manages task delegation
- Specialized agents handle domains (research, analysis, writing)
- Shared context and handoff protocols

→ Source: `claude_agent_sdk/chief_of_staff_agent/`

### Observability Integration
Tracing and monitoring for agent systems.

**Integrations:** Langfuse, custom spans, token tracking

→ Source: `claude_agent_sdk/observability_agent/`

## Design Principles

1. **Start simple** - Use prompt chaining before jumping to complex orchestration
2. **Explicit handoffs** - Clear protocols for agent-to-agent communication
3. **Bounded loops** - Set max iterations to prevent infinite refinement
4. **Fail gracefully** - Agents should handle tool failures and uncertainty
5. **Observability** - Log decisions and tool calls for debugging

## When NOT to Use Agents

- Simple single-turn tasks (use direct API call)
- Latency-critical applications (agents add round-trips)
- Tasks with clear, fixed workflows (use deterministic code)
- When a single well-crafted prompt suffices
