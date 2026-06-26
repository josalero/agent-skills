# Eval: Software Design Analysis

## Prompt

We need to add bulk CSV export for admin users (up to 100k rows). Today exports run synchronously in the API and time out. Analyze options, define acceptance criteria, and recommend an approach before any implementation.

Stack: Spring Boot REST API, PostgreSQL, existing auth. Timeline: one sprint.

## Expected Agent Behavior

- Frames problem and non-goals (e.g. not rebuilding admin UI)
- Lists functional and non-functional requirements with measurable criteria
- Compares at least two options (sync chunking vs async job + download link, etc.)
- Provides tradeoff matrix and incremental recommendation
- Identifies open questions (storage retention, auth on download URLs)
- Does not jump to code or specific class names as the first deliverable

## Failure Signals

- Recommends microservices without justification
- No acceptance criteria or success metrics
- Single option only
- Skips operability (monitoring, failure, rollback)
