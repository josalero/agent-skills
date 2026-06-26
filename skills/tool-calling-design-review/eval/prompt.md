# Eval: Tool Calling Design Review

## Prompt

Review an agent with these tools exposed to the LLM:

1. `run_sql(query: string)` — runs SQL against production read replica
2. `update_user(userId: string, role: string)` — changes user role
3. `send_email(to: string, body: string)` — sends arbitrary email

Authentication is a session cookie on the chat API. Recommend redesign.

## Expected Agent Behavior

- Flags SQL tool as critical risk; recommends parameterized domain tools instead
- Requires server-side authz on update_user; rejects model-supplied userId trust
- Rate limits and confirms send_email; sanitizes recipients to session scope
- Proposes tool split, schemas, idempotency, logging, and confirmation gates
- Provides prioritized findings with severity

## Failure Signals

- Keeps run_sql with "read only" assumption only
- Suggates prompt "do not do bad things" as primary control
- No mention of confirmation for role changes
- Ignores session/auth binding
