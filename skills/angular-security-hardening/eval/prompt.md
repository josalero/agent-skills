# Eval: Angular Security Hardening

## Prompt

Review an Angular app storing JWT in localStorage, using bypassSecurityTrustHtml for user comments, and putting API keys in environment.ts. Prioritize fixes.

## Expected Agent Behavior

- Flags localStorage JWT XSS risk and client-side secrets
- Removes or restricts sanitizer bypass; prefers default binding or server-side sanitization
- Recommends HttpOnly cookies or short-lived memory tokens + refresh
- Mentions interceptors, CSRF if cookies, CSP headers

## Failure Signals

- Keeps bypassTrustHtml for all user content
- Obfuscation instead of removing secrets from client
- Guard-only auth fix
