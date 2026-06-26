# CI/CD, Configuration, and Deploy Smoke Checks

Keep secrets out of git. Run migrations as an explicit deploy step when appropriate.

## CI Pipeline Stages

```yaml
name: ci

on:
  push:
    branches: [main]

jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: shivammathur/setup-php@v2
        with:
          php-version: '8.3'
          extensions: mbstring, pdo_mysql, opcache
      - run: composer install --no-interaction --prefer-dist
      - run: vendor/bin/phpstan analyse
      - run: vendor/bin/phpunit
      - run: composer audit

  image:
    needs: verify
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: docker build -t registry.example.com/shop-api:${{ github.sha }} .
      - run: docker push registry.example.com/shop-api:${{ github.sha }}
```

## Environment Configuration

| Concern | Pattern |
| --- | --- |
| App secrets | Secret manager or CI masked vars |
| Database URL | `DATABASE_URL` env var |
| Laravel config cache | `php artisan config:cache` at deploy |
| Symfony env | `APP_ENV=prod`, warmed cache in deploy job |
| Debug mode | Disabled in production (`APP_DEBUG=false`) |

## Kubernetes Probe Snippet

```yaml
livenessProbe:
  httpGet:
    path: /health/live
    port: 8080
  initialDelaySeconds: 10
readinessProbe:
  httpGet:
    path: /health/ready
    port: 8080
  periodSeconds: 5
```

## Deploy Smoke Check

```bash
IMAGE=registry.example.com/shop-api:${GIT_SHA}
kubectl set image deployment/shop-api app=${IMAGE}
kubectl rollout status deployment/shop-api --timeout=120s
curl -fsS "https://shop-api.example.com/health/ready"
curl -fsS -H "Authorization: Bearer ${SMOKE_TOKEN}" "https://shop-api.example.com/api/v1/orders?page=1"
```

## Migration Job (Laravel)

```bash
php artisan migrate --force --no-interaction
```

Symfony:

```bash
bin/console doctrine:migrations:migrate --no-interaction
```

Run migrations once per deploy, not from every app replica concurrently, unless using a coordinated job.

## Operational Follow-Ups

- Rotate secrets referenced by the new deployment.
- Confirm worker count × DB pool size stays below database max connections.
- Set log shipping and request correlation IDs before scaling traffic.
- Document rollback image tag and migration reversibility constraints.
