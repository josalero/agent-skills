---
name: php-delivery-operations
description: Deliver PHP applications to containers and cloud platforms with health checks, runtime configuration, observability hooks, and CI/CD. Use when dockerizing PHP apps, configuring PHP-FPM or FrankenPHP, tuning workers, setting up deployment pipelines, or preparing Laravel/Symfony services for Kubernetes and cloud runtimes.
---

# PHP Delivery Operations

## Workflow

1. Inspect PHP version, framework, existing Dockerfile, compose files, CI pipeline, web server (nginx, Caddy), and deployment target (Kubernetes, ECS, VM, PaaS).
2. Identify gaps: image size, OPcache config, env-based settings, health endpoints, graceful shutdown, metrics/traces, migrations at deploy, and secret injection.
3. Prefer twelve-factor configuration: environment-specific settings through env vars or secret manager, not baked into images.
4. Configure liveness vs readiness separately — readiness should reflect dependency availability the platform should respect.
5. Tune PHP-FPM/Octane/worker counts against CPU, memory limits, and database connection ceilings.
6. Verify with local container run, health probe checks, CI build/push, and smoke test against the deployed artifact.

## References

- Read `references/containers-and-runtime.md` for Dockerfiles, PHP-FPM, OPcache, and local run patterns.
- Read `references/cicd-and-config.md` for CI/CD stages, env config, secrets, migrations, and deployment smoke checks.

## Delivery Checklist

- Image runs as non-root where possible.
- Config and secrets come from environment or secret store — not the image layer.
- Liveness and readiness probes target meaningful endpoints.
- OPcache is enabled in production with validated revalidation settings.
- Application stops gracefully on SIGTERM within platform timeout.
- Metrics and structured logs are available for the runtime environment.
- CI builds, tests, scans, and produces an immutable image tag or artifact.

## Output

After delivery work, summarize:

- Target runtime and deployment change
- Files added or updated (Dockerfile, CI, K8s manifest, compose)
- Health, config, and runtime decisions
- Commands to build, run locally in container, and deploy
- Operational follow-ups (ingress, autoscaling, DB migrations, secrets rotation)
