# Eval: Production Readiness Review

## Prompt

We plan to launch a new billing integration that charges cards at order completion. Migration adds two columns to `orders`. Staging tests passed; no load test yet. Perform a production readiness review and give go/no-go with blockers.

## Expected Agent Behavior

- Identifies blockers: payment correctness, idempotency, PCI scope, migration risk, missing load test
- Checks observability, rollback, runbook, and hypercare for payment failures
- Separates waivable vs non-waivable gaps
- Outputs checklist-style results and launch/rollback plan

## Failure Signals

- Blanket "go" because staging passed
- No mention of payment idempotency or reconciliation
- Assumes DB migration is always rollbackable
- No metrics or alert guidance
