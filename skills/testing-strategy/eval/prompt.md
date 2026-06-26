# Eval: Testing Strategy

## Prompt

We are adding a webhook delivery feature (HTTP POST to customer URLs on order events). CI currently runs unit tests only; builds take 4 minutes. Propose a test strategy and CI gates for the next two sprints without blowing up pipeline time.

## Expected Agent Behavior

- Identifies risks: SSRF, retries, signature verification, duplicate delivery, customer endpoint failures
- Recommends unit tests for signing/payload + integration with wire mock or test HTTP server
- Suggests contract tests for webhook payload schema
- Defers full E2E or keeps minimal smoke; proposes PR vs main gate split
- Outputs risk matrix and prioritized test list

## Failure Signals

- Suggests only manual QA
- Proposes E2E against real customer URLs
- No mention of SSRF or idempotency testing
- Blanket 90% coverage requirement without rationale
