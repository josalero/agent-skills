---
name: rust-api-service
description: Build, review, refactor, and test Rust web API services with Axum or Actix. Use when working on HTTP handlers, extractors, middleware, validation, OpenAPI, auth, error responses, or API integration tests.
---

# Rust API Service

## Workflow

1. Inspect Rust edition, web framework (Axum/Actix), crate layout, shared state pattern, and test utilities.
2. Identify whether the task is implementation, review, refactor, test coverage, or production behavior.
3. Follow existing router, handler, service, repository, DTO, and middleware patterns.
4. Keep API boundaries explicit: request types, response DTOs, validation, error mapping, pagination.
5. Share state via `Arc<AppState>` or framework-specific injection — avoid global mutable singletons.
6. Verify with unit tests for services and `axum::test` or `actix_web::test` for HTTP contracts.

## References

- Read `references/api-design.md` for handlers, DTOs, validation, pagination, and error responses.
- Read `references/middleware-and-state.md` for shared state, auth middleware, tracing, and extractor patterns.

## Checklist

- Request bodies validated at the boundary (validator crate or custom extractors).
- Stable error response shape across endpoints.
- Handlers remain thin — business logic in service modules.
- Async handlers use proper error types convertible to responses.
- No internal domain types leaked in public JSON without serde control.
- Tests cover happy path, validation failures, and auth failures.

## Output

Summarize files changed, behavior added or fixed, tests added, `cargo test` commands, and API compatibility notes.
