# Containers and PHP Runtime

Use multi-stage builds. Keep Composer dev dependencies out of production images.

## Multi-Stage Dockerfile (Laravel/Symfony)

```dockerfile
FROM composer:2 AS vendor
WORKDIR /app
COPY composer.json composer.lock ./
RUN composer install --no-dev --no-interaction --prefer-dist --optimize-autoloader

FROM php:8.3-fpm-bookworm AS runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
        git unzip libzip-dev \
    && docker-php-ext-install opcache pdo_mysql \
    && rm -rf /var/lib/apt/lists/*

COPY docker/php/opcache.ini /usr/local/etc/php/conf.d/opcache.ini
COPY --from=vendor /app/vendor /var/www/html/vendor
COPY . /var/www/html

RUN useradd -u 10001 -r appuser \
    && chown -R appuser:appuser /var/www/html
USER appuser

WORKDIR /var/www/html
```

## OPcache Production Defaults

```ini
opcache.enable=1
opcache.validate_timestamps=0
opcache.max_accelerated_files=20000
opcache.memory_consumption=256
opcache.interned_strings_buffer=16
```

Use `validate_timestamps=1` in local/dev only.

## nginx + PHP-FPM Compose Service

```yaml
services:
  web:
    image: nginx:1.27-alpine
    ports:
      - "8080:80"
    volumes:
      - ./docker/nginx/default.conf:/etc/nginx/conf.d/default.conf:ro
    depends_on:
      - app
  app:
    build: .
    environment:
      APP_ENV: production
      DATABASE_URL: ${DATABASE_URL:?}
    healthcheck:
      test: ["CMD-SHELL", "cgi-fcgi -bind -connect 127.0.0.1:9000 || exit 1"]
      interval: 10s
      timeout: 3s
      retries: 3
```

## Health Endpoints

Laravel:

```php
Route::get('/health/live', fn () => response()->noContent());
Route::get('/health/ready', function () {
    DB::connection()->getPdo();
    return response()->json(['status' => 'ready']);
});
```

Symfony:

```yaml
# config/routes/health.yaml
health_live:
  path: /health/live
  controller: App\Controller\HealthController::live
health_ready:
  path: /health/ready
  controller: App\Controller\HealthController::ready
```

Point readiness at dependencies; keep liveness lightweight.

## Graceful Shutdown

Ensure PHP-FPM `process_control_timeout` and platform termination grace period allow in-flight requests to finish. For queue workers:

```bash
php artisan queue:work --max-time=3600 --stop-when-empty
```

Symfony Messenger:

```bash
bin/console messenger:consume async --time-limit=3600 --memory-limit=256M
```

## Local Verification

```bash
docker build -t shop-api:local .
docker run --rm -p 8080:8080 -e DATABASE_URL="$DATABASE_URL" shop-api:local
curl -fsS http://localhost:8080/health/ready
```
