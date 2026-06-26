# Eval: React Security Hardening

## Prompt

Review a React app that stores JWT in localStorage, renders user bio with dangerouslySetInnerHTML, and passes API key via VITE_OPENAI_KEY. Recommend fixes prioritized by severity.

## Expected Agent Behavior

- Flags localStorage JWT XSS risk and public VITE secret
- Replaces unsafe HTML with sanitization or plain text
- Recommends HttpOnly cookie or memory token strategy with server enforcement
- Mentions CSP, npm audit, CSRF if cookies used
- Prioritizes findings critical/high/medium

## Failure Signals

- Suggests obfuscation instead of removing client secret
- Keeps dangerouslySetInnerHTML with "trust users"
- Client-only auth guard as sole fix
