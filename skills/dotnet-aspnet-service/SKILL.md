---
name: dotnet-aspnet-service
description: Build, review, refactor, and test ASP.NET Core backend services. Use when working on Minimal APIs or controllers, dependency injection, validation, ProblemDetails, configuration, middleware, auth integration, or service-layer tests.
---

# .NET ASP.NET Service

## Workflow

1. Inspect target framework (`net8.0`, `net9.0`), ASP.NET Core version, project layout, DI registration style, and existing test patterns.
2. Identify whether the task is implementation, review, refactor, test coverage, or production behavior.
3. Follow existing controller/endpoint, service, repository, DTO, validation, and configuration patterns.
4. Keep API boundaries explicit: request models, response DTOs, validation, ProblemDetails, pagination, and compatibility.
5. Register services in `Program.cs` or extension methods — prefer constructor injection; avoid service locator.
6. Verify with focused unit tests for services and `WebApplicationFactory` or `WebApplicationFactory`-style integration tests when HTTP contracts matter.

## References

- Read `references/api-design.md` for endpoints, DTOs, validation, pagination, and ProblemDetails.
- Read `references/dependency-injection-and-services.md` for DI lifetimes, service layering, and middleware patterns.

## Checklist

- Request models validated at the boundary (`[Required]`, FluentValidation, or data annotations).
- Stable ProblemDetails shape across endpoints; domain exceptions mapped in one place.
- Services do not reference `HttpContext` directly — pass primitives or scoped context objects.
- Async all the way with `CancellationToken` from the request.
- No entity types returned from endpoints — use response DTOs.
- Tests cover happy path, validation failures, and not-found or conflict cases.

## Output

Summarize files changed, behavior added or fixed, tests added and why each type was chosen, `dotnet test` commands to run, and API compatibility or migration notes.
