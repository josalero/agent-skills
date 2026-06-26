---
name: dotnet-security-hardening
description: Secure .NET and ASP.NET Core applications during implementation and review. Use when hardening authentication, authorization, input validation, secrets handling, logging, error responses, dependency vulnerabilities, or reviewing security-sensitive C# code.
---

# .NET Security Hardening

## Workflow

1. Inspect target framework, auth model (cookies, JWT, OIDC), authorization policies, and existing security middleware.
2. Identify the threat surface: public endpoints, auth boundaries, data access, file I/O, deserialization, background jobs, and admin paths.
3. Classify the task as implementation, review, incident fix, or dependency remediation.
4. Apply least privilege: authenticate callers, authorize every protected action on the server, validate input at boundaries, and parameterize data access.
5. Protect secrets and sensitive data — never log, expose, or commit credentials, tokens, or PII in unsafe places.
6. Return safe error responses that do not leak stack traces, SQL, paths, or internal identifiers to untrusted clients.
7. Verify with security-focused tests and `dotnet list package --vulnerable`.

## References

- Read `references/auth-and-authorization.md` for JWT, policies, and endpoint protection.
- Read `references/secrets-and-validation.md` for secrets management, input validation, and safe logging.

## Security Checklist

- Authentication enforced before business logic on protected routes.
- Authorization checked server-side for every sensitive operation.
- User input validated and bounded; output encoded where rendered.
- EF and raw SQL use parameters — never string concatenation with user input.
- Secrets from environment, Azure Key Vault, or secret manager — not source code.
- Logs and exceptions do not expose credentials, tokens, or regulated personal data.
- Dependencies with known critical CVEs identified and upgraded or mitigated.
- Security regressions have focused tests where behavior is machine-verifiable.

## Output

Summarize threat addressed, files changed and control added, residual risk, tests or verification commands run, and follow-up items needing manual or infra review.
