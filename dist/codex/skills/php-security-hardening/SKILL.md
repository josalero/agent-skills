---
name: php-security-hardening
description: Secure PHP and Laravel/Symfony applications during implementation and review. Use when hardening authentication, authorization, input validation, persistence access, secrets handling, logging, error responses, dependency vulnerabilities, file uploads, or reviewing security-sensitive PHP code.
---

# PHP Security Hardening

## Workflow

1. Inspect the PHP version, framework (plain PHP, Laravel, Symfony), auth libraries, session config, and existing security middleware.
2. Identify the threat surface: public endpoints, auth boundaries, data access, file/network I/O, deserialization, background jobs, admin paths, and CLI commands.
3. Classify the task as implementation, review, incident fix, or dependency remediation.
4. Apply least privilege: authenticate callers, authorize every protected action on the server, validate input at boundaries, and parameterize data access.
5. Protect secrets and sensitive data: never log, expose, or persist credentials, tokens, or PII in unsafe places.
6. Return safe error responses that do not leak stack traces, SQL, paths, or internal identifiers to untrusted clients.
7. Verify with security-focused tests, static checks, and the narrowest useful test command.

## References

- Read `references/input-and-auth.md` for validation, CSRF, sessions, policies, and injection prevention.
- Read `references/secrets-logging-errors.md` for secrets management, log redaction, and safe API error handling.

## Security Checklist

- Authentication is enforced before business logic on protected routes.
- Authorization is checked server-side for every sensitive operation.
- User input is validated and bounded; output is encoded where rendered.
- SQL and ORM queries use parameters, never string concatenation with user input.
- Secrets come from environment or secret manager — not source code.
- Logs and exceptions do not expose credentials, tokens, or regulated personal data.
- Dependencies with known critical CVEs are identified and upgraded or mitigated.
- Security regressions have focused tests where behavior is machine-verifiable.

## Output

After security work, summarize:

- Threat or vulnerability addressed
- Files changed and control added (auth, validation, query, logging, config)
- Residual risk and assumptions
- Tests or verification commands run
- Follow-up items that need manual review or infra change
