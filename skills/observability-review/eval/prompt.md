# Eval: Observability Review

## Prompt

Our team gets paged nightly for "CPU > 80%" on a Java API pod, but users report no issues. Incidents take 45 minutes because logs are plain text without trace IDs. Review observability and recommend improvements.

## Expected Agent Behavior

- Identifies alert misalignment (infra metric without user impact)
- Recommends structured logs with trace/correlation IDs
- Proposes golden signals dashboard and symptomatic alerts (error rate, latency SLO)
- Addresses cardinality and runbook gaps
- Prioritizes quick wins vs longer SLO work

## Failure Signals

- Suggests only "add more logs"
- Keeps CPU-only paging without tuning threshold or pairing with latency/errors
- Recommends logging full request bodies
- No runbook or dashboard guidance
