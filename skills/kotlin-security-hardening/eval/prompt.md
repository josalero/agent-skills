# Eval: Kotlin Security Hardening

## Prompt

Review our Kotlin Spring Boot user API. The delete endpoint lacks authorization, password reset logs the token, and one repository method builds SQL with string concatenation. Harden without breaking existing integration tests.

## Expected Agent Behavior

- Adds method-level or URL authorization
- Removes sensitive data from logs
- Replaces dynamic SQL with parameterized queries
- Adds security-focused tests where verifiable

## Failure Signals

- Disables security filters globally
- Leaves token logging in place
- Only adds client-side checks
