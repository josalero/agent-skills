# Eval: Agent Orchestration Design

## Prompt

We want an "onboarding agent" that reads HR docs (RAG), creates accounts in three SaaS tools via API, sends a Slack welcome, and assigns training tasks. Product asked for "one autonomous GPT agent." We're on Spring Boot with a REST chat API today (single LLM call + RAG). Design the orchestration architecture.

## Expected Agent Behavior

- Questions whether single autonomous loop is appropriate vs workflow with LLM steps + deterministic integration steps
- Proposes topology (likely workflow with supervised tool phases or handoffs) — not unbounded agent
- Separates read (RAG) from mutating tools; requires HITL or confirmation for account creation
- Defines state ownership, idempotency for creates, step/time limits
- Mentions async job for long runs and user progress visibility
- References tool-calling and eval for multi-step golden paths
- Warns against storing credentials in agent context

## Failure Signals

- "Single GPT agent handles everything" with no limits or HITL
- No idempotency for account creation retries
- RAG and mutating tools in one undifferentiated loop without authz discussion
- No simpler workflow alternative considered
- No observability or eval for tool sequence
