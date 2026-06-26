# Eval: Security Review

## Prompt

Perform a security review of a multi-tenant SaaS API where tenants are identified by subdomain (`{tenant}.app.example.com`) and JWT contains `tenantId` and `role`. Users manage projects scoped to their tenant. Focus on authorization, token trust, and data isolation.

## Expected Agent Behavior

- Maps trust boundaries and IDOR/multi-tenant isolation risks
- Questions whether `tenantId` in JWT is validated against subdomain/host
- Checks project listing and detail endpoints for cross-tenant access
- Covers logging, error messages, admin bypass, and dependency/config basics
- Outputs prioritized findings with exploit scenarios and verification steps
- Avoids echoing PII or secrets in the review

## Failure Signals

- Generic OWASP list with no tenant-specific analysis
- Suggests "use HTTPS" as primary finding only
- Misses JWT/subdomain mismatch attack
- No severity or verification guidance
