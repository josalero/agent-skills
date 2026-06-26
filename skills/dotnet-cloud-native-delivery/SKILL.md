---
name: dotnet-cloud-native-delivery
description: Deliver .NET services to containers and cloud platforms with health checks, configuration, observability hooks, and CI/CD. Use when dockerizing ASP.NET Core apps, configuring liveness/readiness probes, tuning container resources, setting up deployment pipelines, or preparing services for Kubernetes.
---

# .NET Cloud Native Delivery

## Workflow

1. Inspect build output, target framework, existing Dockerfile, compose files, CI pipeline, and deployment target (Kubernetes, Azure Container Apps, ECS).
2. Identify gaps: image size, publish mode, config via env vars, health endpoints, graceful shutdown, metrics/traces, and secret injection.
3. Prefer twelve-factor configuration: environment-specific settings through env vars or config service, not baked into images.
4. Configure liveness vs readiness separately — readiness should reflect dependency availability the platform should respect.
5. Set container-aware resource limits and validate memory against GC heap, native overhead, and request concurrency.
6. Verify with local container run, health probe checks, CI build/push, and smoke test against the deployed artifact.

## References

- Read `references/containers-and-health.md` for Dockerfiles, health checks, and graceful shutdown.
- Read `references/kubernetes-and-cicd.md` for K8s probes, manifests, and CI/CD stages.

## Delivery Checklist

- Image runs as non-root where possible.
- Config and secrets from environment or secret store — not the image layer.
- Liveness and readiness probes target meaningful endpoints.
- Application stops gracefully on SIGTERM within platform timeout.
- Metrics and structured logs available for the runtime environment.
- CI builds, tests, scans, and produces an immutable image tag or artifact.

## Output

Summarize target runtime and deployment change, files added or updated, health/config/resource decisions, commands to build and run locally in container, and operational follow-ups (ingress, autoscaling, migrations, secrets rotation).
