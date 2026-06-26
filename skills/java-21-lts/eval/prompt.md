# Eval: Java 21 LTS

## Prompt

This Gradle service still targets Java 17. Upgrade the project to Java 21, then refactor the audit trail helper to use sequenced collection APIs and pattern matching for switch. Evaluate whether the HTTP export path should use virtual threads.

Hints:

- `build.gradle.kts` uses `JavaLanguageVersion.of(17)`
- CI uses `java-version: '17'`
- Dockerfile uses `eclipse-temurin:17-jre`
- `AuditTrail` uses `events.get(0)` and manual list reversal
- `EventFormatter` uses `if/else instanceof` chains on a sealed `AuditEvent` hierarchy
- Export fan-out is blocking HTTP to ~200 endpoints per batch

## Expected Agent Behavior

- Updates Gradle toolchain, CI, and Docker to Java 21 before source refactors
- Replaces first/last/reverse helpers with sequenced collection methods where appropriate
- Refactors sealed event handling to an exhaustive `switch` with pattern matching
- Treats virtual threads as optional: recommends measurement for blocking HTTP, warns about pinning and CPU-bound misuse
- Runs focused compile/test commands and summarizes versions, files changed, and verification steps
- Does not enable preview features

## Failure Signals

- Changes source before build targets 21
- Updates only one of Gradle, CI, or Docker
- Enables virtual threads without discussing blocking I/O suitability
- Rewrites unrelated modules or adopts string templates preview
- Skips test verification
