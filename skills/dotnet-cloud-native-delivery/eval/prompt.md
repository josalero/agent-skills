# Eval: .NET Cloud Native Delivery

## Prompt

Dockerize an ASP.NET Core 9 API for Kubernetes. The app uses PostgreSQL and already has `AddHealthChecks().AddNpgSql(...)`. Provide a production-oriented Dockerfile, separate liveness/readiness endpoints, and a Deployment snippet with probes. CI is GitHub Actions.

Requirements: non-root container user, env-based connection string, graceful shutdown consideration, immutable image tags.

## Expected Agent Behavior

- Multi-stage Dockerfile with SDK build and aspnet runtime
- Maps `/health/live` and `/health/ready` with appropriate predicates
- K8s liveness vs readiness probes on different paths
- Secrets via `Secret`/`envFrom`, not baked into image
- CI builds, tests, publishes, and tags image with commit SHA
- Mentions migration job or init container and smoke test after deploy

## Failure Signals

- Single-stage Dockerfile with SDK in production image
- Same health endpoint for liveness and readiness with DB check on liveness
- Runs as root with no resource limits
- Uses `:latest` as only deploy tag
- Connection string hardcoded in Dockerfile ENV
