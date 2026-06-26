# Eval: PHP Delivery Operations

## Prompt

This Laravel API needs to run on Kubernetes. Add or fix container packaging, health probes configuration, PHP runtime settings, and document the CI deploy smoke check. The repo currently only runs with `php artisan serve`.

Provide Dockerfile changes, example Kubernetes probe snippets, and required env vars.

## Expected Agent Behavior

- Produces multi-stage Dockerfile with PHP-FPM or suitable runtime and non-root user
- Enables OPcache for production and documents env-based database config
- Separates liveness and readiness using lightweight and dependency-aware endpoints
- Configures graceful shutdown for FPM/workers and documents queue worker deploy if used
- Outlines CI stages with immutable image tag and post-deploy smoke test
- Summarizes local `docker build` / `docker run` commands

## Failure Signals

- Uses development server (`artisan serve`) as production entrypoint
- Runs container as root with no comment
- Points liveness probe at endpoint that hits the database
- Hardcodes secrets in Dockerfile or committed compose file
- Omits readiness check for DB-dependent service
