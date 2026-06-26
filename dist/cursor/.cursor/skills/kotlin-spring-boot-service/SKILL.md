---
name: kotlin-spring-boot-service
description: Build, review, refactor, and test Spring Boot backend services written in Kotlin. Use when working on REST controllers, dependency injection, validation, ProblemDetail responses, configuration, coroutine endpoints, transactions, or service-layer tests.
---

# Kotlin Spring Boot Service

## Workflow

1. Inspect Kotlin version, Spring Boot BOM, build tool, package layout, and existing test patterns.
2. Identify whether the task is implementation, review, refactor, test coverage, or production behavior.
3. Follow existing controller, service, repository, DTO, validation, and configuration patterns.
4. Keep API boundaries explicit: request models, response DTOs, validation, error responses, pagination, and compatibility.
5. Prefer constructor injection; use Kotlin data classes for DTOs; keep entities off public API surfaces.
6. Verify with focused unit tests for services and `@WebMvcTest` or `@SpringBootTest` when HTTP contracts matter.

## References

- Read `references/api-design.md` for controllers, DTOs, validation, pagination, and ProblemDetail handling.
- Read `references/dependency-injection-and-services.md` for DI lifetimes, service layering, transactions, and coroutine integration.

## Checklist

- Request models validated at the boundary (`@Valid`, Jakarta validation, or custom validators).
- Stable error response shape across endpoints; domain exceptions mapped in one place.
- Services do not reference `HttpServletRequest` directly — pass primitives or scoped context objects.
- Suspend endpoints use structured concurrency; blocking I/O stays off event-loop threads when using WebFlux.
- No entity types returned from endpoints — use response DTOs.
- Tests cover happy path, validation failures, and not-found or conflict cases.

## Output

Summarize files changed, behavior added or fixed, tests added and why each type was chosen, `./gradlew test` commands to run, and API compatibility or migration notes.
