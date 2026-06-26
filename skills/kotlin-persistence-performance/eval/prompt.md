# Eval: Kotlin Persistence Performance

## Prompt

Our Kotlin Spring Boot order list endpoint takes 4s with 200 orders. Hibernate SQL log shows 201 queries. Diagnose the N+1, fix fetch strategy or projection, and add an integration test that fails if query count regresses.

## Expected Agent Behavior

- Identifies N+1 from SQL evidence
- Applies fetch join, entity graph, or DTO projection
- Adds query-count or integration regression test
- Avoids over-fetching unrelated associations

## Failure Signals

- Enables eager fetch globally without analysis
- Fixes symptom with cache without addressing query count
- No regression test
