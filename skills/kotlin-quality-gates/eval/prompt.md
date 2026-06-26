# Eval: Kotlin Quality Gates

## Prompt

Enable detekt and ktlint in our Kotlin Gradle CI. Fix violations in the Auth module without disabling rules globally or removing JaCoCo coverage on service packages.

## Expected Agent Behavior

- Wires detekt/ktlint into check task
- Runs ./gradlew check locally
- Fixes or narrowly suppresses violations with rationale
- Keeps tests green

## Failure Signals

- Disables detekt globally
- Removes coverage verification
- Skips formatting check after enabling it
