# Eval: Java JVM Debugging

## Prompt

Production alert: p95 latency doubled after deploy. Heap usage climbs over 4 hours until pod restart. Thread dump shows 180 threads blocked on `HikariPool.getConnection`. GC logs show frequent young GC but old gen is stable.

Investigate likely causes, propose the next evidence to collect, and suggest reversible fixes. Do not recommend blind heap or GC tuning yet.

## Expected Agent Behavior

- Starts from symptom and recent deploy change
- Separates JVM tuning from connection pool / downstream DB issues
- Requests or interprets pool metrics, SQL latency, and thread dump evidence
- Proposes reversible fixes (pool sizing, leak check, query timeout) with rollback
- Documents hypothesis, evidence, change, and success metric
- Avoids speculative `-Xmx` changes without heap dump or allocation evidence

## Failure Signals

- Jumps straight to GC algorithm changes
- Ignores connection pool blocked threads
- Suggests production heap dump without caution or approval path
- Does not define how to verify recovery
