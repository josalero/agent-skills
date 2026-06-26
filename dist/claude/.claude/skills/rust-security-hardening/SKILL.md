---
name: rust-security-hardening
description: Secure Rust web services and libraries during implementation and review. Use when hardening authentication, authorization, input validation, SQL access, secrets handling, logging, error responses, dependency advisories, or reviewing security-sensitive Rust code.
---

# Rust Security Hardening

## Workflow

1. Inspect framework (Axum/Actix), auth crates, TLS setup, and secret loading patterns.
2. Identify threat surface: public routes, auth middleware, database access, file I/O, deserialization, and admin endpoints.
3. Classify task as implementation, review, incident fix, or dependency remediation.
4. Apply least privilege: authenticate, authorize on server, validate at boundaries, parameterize queries.
5. Protect secrets — use environment or secret manager; never commit credentials.
6. Return safe error responses without leaking internal paths or query details.
7. Run `cargo audit` or `cargo deny` and verify with security-focused tests.

## References

- Read `references/auth-and-validation.md` for JWT, API keys, extractor validation, and rate limiting.
- Read `references/data-access-and-secrets.md` for parameterized SQL, secret loading, and safe logging.

## Security Checklist

- Auth enforced on protected routes before handler logic.
- Authorization checked per resource, not only authentication.
- Input validated and size-bounded at HTTP boundary.
- SQL uses bind parameters exclusively.
- Secrets not in source, logs, or error JSON to clients.
- Critical advisories triaged from `cargo audit` / deny.
- Security regressions covered by tests where machine-verifiable.

## Output

Summarize threat addressed, files changed, residual risk, audit commands run, and follow-up items.
