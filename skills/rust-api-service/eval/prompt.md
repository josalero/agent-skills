# Eval: Rust API Service

## Prompt

Add POST /api/v1/orders to our Axum service. Validate JSON input, return OrderResponse DTO, map OrderNotFound to 404 JSON error, and add handler tests for validation and not-found cases.

## Expected Agent Behavior

- Uses typed request/response structs with serde
- Centralizes ApiError to response mapping
- Adds axum::test or similar HTTP tests
- Runs cargo test on api crate

## Failure Signals

- Returns internal types directly in JSON
- Panics in handlers on expected errors
- Skips validation failure tests
