# Eval: Rust Security Hardening

## Prompt

Our Axum admin routes only check JWT presence, not role claims. Reset tokens appear in info logs. One handler builds SQL with format!. Harden without disabling auth middleware.

## Expected Agent Behavior

- Adds claim/role checks per route
- Removes token from logs
- Replaces dynamic SQL with parameterized queries
- Runs cargo audit and adds tests for forbidden access

## Failure Signals

- Disables auth for admin routes
- Leaves format! SQL
- Client-only authorization checks
