# CI Pipeline Gates for Kotlin

## Typical PR Stage

```yaml
- run: ./gradlew check --no-daemon
```

## Stage Separation

| Stage | Purpose |
| --- | --- |
| compile + unit test | Fast feedback on every PR |
| detekt/ktlint | Static style and complexity |
| integration test | Main branch or nightly when slow |
| coverage gate | JaCoCo thresholds on service packages |

## Reproducing CI Locally

Match JDK via `jenv shell` or Gradle toolchain. Use `--no-daemon` in CI for consistency.
