# Eval: Java Migrate Any Version

## Prompt

Migrate this Maven project from Java 17 to Java 21. Update build files, CI workflow snippet, and Docker base image. Identify source or dependency blockers. Run tests incrementally.

Current hints:

- `pom.xml` uses `<maven.compiler.release>17</maven.compiler.release>`
- CI uses `java-version: '17'`
- Dockerfile uses `eclipse-temurin:17-jre`
- One test fails on 21 with `javax.annotation` import in a third-party wrapper

## Expected Agent Behavior

- Reads migration path references before editing
- Updates build config first, then CI/container, then source/dependencies
- Proposes focused test command after each step
- Handles `javax` to Jakarta or dependency upgrade explicitly
- Summarizes versions changed, blockers, and remaining follow-ups
- Does not adopt preview features or virtual threads in the same PR

## Failure Signals

- Changes source before build compiles on 21
- Updates JDK in only one of pom, CI, and Docker
- Skips test verification between steps
- Removes failing test instead of fixing compatibility
