---
name: angular-security-hardening
description: Secure Angular applications against XSS, unsafe HTML binding, token exposure, CSRF, and insecure API usage. Use when reviewing SPA auth, sanitization bypass, interceptors, or client-side secret handling in Angular apps.
---

# Angular Security Hardening

## Workflow

1. Map trust boundaries: template bindings, innerHTML, dynamic URLs, localStorage, third-party scripts.
2. Prefer Angular sanitization defaults — avoid bypassing unless strictly controlled and documented.
3. Store tokens in HttpOnly cookies when backend supports it; never embed API secrets in environment.ts for production private keys.
4. Use HTTP interceptors for auth headers and CSRF tokens on mutating requests.
5. Enforce authorization on APIs — route guards are UX only.
6. Audit dependencies (`npm audit`) and keep Angular patched for security releases.
7. Configure CSP and security headers at hosting layer — not only client code.

## References

- Read `references/xss-and-sanitization.md` for DomSanitizer, binding rules, and template safety.
- Read `references/auth-interceptors-csrf.md` for interceptors, cookies, and CSRF patterns.

## Checklist

- No private secrets in client bundle environments.
- `[innerHTML]` only with sanitized, trusted content policy.
- `javascript:` URLs blocked in dynamic links.
- HttpOnly session cookies + CSRF header when using cookie auth.
- Guards complemented by server-side authorization tests.
- Logout clears client state and invalidates server session.

## Output

Summarize threats, code/config changes, residual risks, and verification steps.
