# Eval: Java Cloud Native Delivery

## Prompt

This Spring Boot service needs to run on Kubernetes. Add or fix container packaging, health probes configuration, JVM container settings, and document the CI deploy smoke check. The repo currently only runs with `./gradlew bootRun`.

Provide Dockerfile changes, example Kubernetes probe snippets, and required env vars.

## Expected Agent Behavior

- Produces multi-stage Dockerfile with JRE runtime and non-root user
- Sets container-aware JVM flags (`MaxRAMPercentage` or equivalent)
- Separates liveness and readiness using Actuator probe endpoints
- Configures graceful shutdown and documents env-based datasource config
- Outlines CI stages with immutable image tag and post-deploy smoke test
- Summarizes local `docker build` / `docker run` commands

## Failure Signals

- Uses JDK image in final stage without reason
- Runs container as root with no comment
- Points liveness probe at `/api` endpoint that hits the database
- Hardcodes secrets in Dockerfile or committed compose file
- Omits readiness check for DB-dependent service
