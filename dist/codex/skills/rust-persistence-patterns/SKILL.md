---
name: rust-persistence-patterns
description: Design and optimize persistence layers with sqlx and Diesel in Rust services. Use when modeling queries, transactions, connection pools, migrations, N+1 patterns, compile-time query checks, or async database access.
---

# Rust Persistence Patterns

## Workflow

1. Identify the persistence library in use: sqlx, Diesel, or both in a workspace.
2. Inspect pool configuration, migration strategy, and transaction boundaries in handlers/services.
3. Prefer parameterized queries and compile-time checked SQL where sqlx macros are used.
4. Keep repository modules as the only database touchpoint — handlers stay thin.
5. Optimize hot paths: batch inserts, pagination, indexes, and connection pool sizing.
6. Verify with integration tests against real Postgres (Testcontainers or CI service).

## References

- Read `references/sqlx-patterns.md` for pools, queries, transactions, and migrations with sqlx.
- Read `references/diesel-patterns.md` for schema modeling, query DSL, and connection management.

## Checklist

- All queries parameterized — no format! with user input.
- Transactions scoped to business operations — not entire requests by default.
- Pool max connections sized for instance count and DB limits.
- Migrations versioned and applied in CI/deploy pipeline.
- Integration tests cover critical queries and constraint behavior.
- N+1 avoided via joins or batched loads.

## Output

Summarize schema or query changes, pool settings, tests added, and `cargo test` commands.
