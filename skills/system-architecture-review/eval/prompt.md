# Eval: System Architecture Review

## Prompt

We are considering splitting our monolithic Spring Boot app into separate Order and Inventory services. Both currently share one PostgreSQL database and deploy together weekly. Review this proposal and recommend whether to split now, later, or not at all. Identify risks and a smallest next step.

## Expected Agent Behavior

- Maps current coupling (shared DB, release cadence, transactional boundaries)
- Asks about consistency requirements for order + inventory updates
- Identifies distributed monolith risk if DB stays shared
- Compares sync vs async inventory reservation options
- Recommends phased approach (e.g., module boundaries first, strangler, or defer split)
- Outputs structured findings with severity and verification spikes

## Failure Signals

- Recommends microservices without addressing shared database
- Ignores operational cost (deploy, observe, on-call)
- No tradeoff section or open questions
- Assumes split is always correct
