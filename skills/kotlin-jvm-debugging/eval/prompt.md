# Eval: Kotlin JVM Debugging

## Prompt

Our Kotlin Spring Boot service memory grows 200MB/hour under steady traffic. Thread dumps show thousands of RUNNABLE coroutines on Dispatchers.IO. Diagnose and propose a fix with measurable verification.

## Expected Agent Behavior

- Collects GC logs and thread/coroutine evidence
- Identifies scope or pool misuse vs true heap leak
- Proposes reversible fix with metric to confirm
- Documents rollback plan

## Failure Signals

- Suggests random JVM flags without evidence
- Ignores coroutine scope lifecycle
- No verification metric proposed
