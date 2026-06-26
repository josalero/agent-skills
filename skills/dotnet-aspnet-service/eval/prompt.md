# Eval: .NET ASP.NET Service

## Prompt

Add a POST `/api/v1/orders` endpoint that accepts `sku` and `quantity`, validates input, persists an order, and returns `201` with order id and status. Follow existing project patterns. Include service unit tests and an integration test for the HTTP contract.

Existing stack: ASP.NET Core 8, EF Core, xUnit, FluentValidation or data annotations.

## Expected Agent Behavior

- Inspects `Program.cs`, existing endpoints, DTOs, DI registration, and tests first
- Uses request/response DTOs instead of exposing EF entities
- Validates at the boundary and returns ProblemDetails for errors
- Registers services with appropriate lifetimes (scoped repository/service)
- Adds unit test for service rules and `WebApplicationFactory` test for `400` on invalid quantity
- Summarizes files changed, tests added, and `dotnet test` command

## Failure Signals

- Returns `OrderEntity` from the endpoint
- No validation on request body
- Maps exceptions inline in every endpoint instead of centralized handler
- Missing test for blank sku or quantity out of range
