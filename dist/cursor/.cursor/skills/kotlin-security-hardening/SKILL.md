---
name: kotlin-security-hardening
description: Secure Kotlin and Spring Boot applications during implementation and review. Use when hardening authentication, authorization, input validation, persistence access, secrets handling, logging, error responses, dependency vulnerabilities, or reviewing security-sensitive Kotlin code.
---

# Kotlin Security Hardening

## Workflow

1. Inspect Kotlin version, framework (Ktor, Spring Boot), security libraries, auth model, and existing security configuration.
2. Identify the threat surface: public endpoints, auth boundaries, data access, file/network I/O, deserialization, background jobs, and admin paths.
3. Classify the task as implementation, review, incident fix, or dependency remediation.
4. Apply least privilege: authenticate callers, authorize every protected action on the server, validate input at boundaries, and parameterize data access.
5. Protect secrets and sensitive data: never log, expose, or persist credentials, tokens, or PII in unsafe places.
6. Return safe error responses that do not leak stack traces, SQL, paths, or internal identifiers to untrusted clients.
7. Verify with security-focused tests and the narrowest useful build or test command.

## References

- Read `references/spring-security.md` for Spring Security filter chains, method security, CSRF, sessions, and JWT patterns.
- Read `references/input-and-data-access.md` for validation, injection prevention, and safe persistence/query patterns.

## Security Checklist

- Authentication enforced before business logic on protected routes.
- Authorization checked server-side for every sensitive operation.
- User input validated and bounded; output encoded where rendered.
- SQL/JPQL/native queries use parameters, never string concatenation with user input.
- Secrets come from environment or secret manager — not source code.
- Logs and exceptions do not expose credentials, tokens, or regulated personal data.
- Dependencies with known critical CVEs are identified and upgraded or mitigated.

## Output

Summarize threat addressed, files changed, residual risk, tests run, and follow-up items needing manual review.
