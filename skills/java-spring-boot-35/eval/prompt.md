# Eval: Java Spring Boot 3.5

## Prompt

Upgrade this Spring Boot 3.4.2 / Java 21 service to Spring Boot 3.5.x. Fix any failing tests after the BOM bump. Document breaking changes you hit (boolean properties, actuator defaults, TestRestTemplate redirects).

## Expected Agent Behavior

- Reads `build.gradle.kts` or `pom.xml` before changing versions
- Bumps to latest 3.5.x patch, not Boot 4
- Consults 3.5 breaking changes (`.enabled` values, profiles, heapdump)
- Runs tests and reports `./gradlew test` or `mvn verify` results
- Does not introduce Jackson 3 or Framework 7 APIs

## Failure Signals

- Jumps directly to Spring Boot 4.0
- Changes application code without running tests
- Ignores startup property binding warnings
- Enables preview or Boot 4-only features on a 3.5 target
