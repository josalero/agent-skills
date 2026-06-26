# Eval: Kotlin Migrate Any Version

## Prompt

Plan and execute upgrading our multi-module Gradle project from Kotlin 1.9 to Kotlin 2.1. Several modules use kotlinx.serialization and coroutines. CI must stay green and JVM target remains 21.

## Expected Agent Behavior

- Produces phased plan before bulk edits
- Aligns kotlinx library versions with Kotlin 2.1
- Fixes compile errors incrementally
- Updates CI workflow JDK/Kotlin references
- Documents rollback steps

## Failure Signals

- Bumps Kotlin without checking Spring/Ktor compatibility
- Leaves mismatched JVM targets across modules
- Skips test verification
