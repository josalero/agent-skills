# Eval: Kotlin Spring Boot Service

## Prompt

Add a POST `/api/v1/orders` endpoint to our Kotlin Spring Boot service. Validate input, return a response DTO (not entities), map `OrderNotFoundException` to ProblemDetail 404, and add service unit tests plus a WebMvcTest for validation failures.

## Expected Agent Behavior

- Uses data class DTOs and constructor injection
- Centralizes exception mapping in ControllerAdvice
- Adds focused unit and slice tests
- Runs ./gradlew test for affected modules

## Failure Signals

- Returns JPA entities from the controller
- Scatters validation logic in the controller
- Skips tests for 404 and validation cases
