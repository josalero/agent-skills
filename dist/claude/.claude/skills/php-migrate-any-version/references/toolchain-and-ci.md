# Toolchain, CI, and Container Migration

Change platform constraints before mass-editing source files.

## Composer Platform Requirements

```json
{
  "require": {
    "php": "^8.3"
  },
  "config": {
    "platform": {
      "php": "8.3.12"
    }
  }
}
```

After bumping PHP:

```bash
composer update --with-all-dependencies
composer validate --strict
```

## PHPUnit and Static Analysis

```xml
<!-- phpunit.xml -->
<phpunit bootstrap="vendor/autoload.php" cacheDirectory=".phpunit.cache">
  <testsuites>
    <testsuite name="unit">
      <directory>tests/Unit</directory>
    </testsuite>
  </testsuites>
  <php>
    <env name="APP_ENV" value="testing"/>
  </php>
</phpunit>
```

```neon
# phpstan.neon
parameters:
    level: 8
    paths:
        - src
        - app
```

## CI Workflow Snippet

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: shivammathur/setup-php@v2
        with:
          php-version: '8.3'
          extensions: mbstring, pdo_mysql
          coverage: none
      - run: composer install --no-interaction --prefer-dist
      - run: vendor/bin/phpstan analyse
      - run: vendor/bin/phpunit
```

## Docker Base Image

Before:

```dockerfile
FROM php:8.1-fpm
```

After:

```dockerfile
FROM php:8.3-fpm-bookworm

RUN docker-php-ext-install pdo_mysql opcache \
    && mv "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini"
```

## Incremental Verification Order

1. Update `composer.json` PHP constraint and CI image.
2. Run `composer update` locally on target PHP.
3. Fix fatal errors and static analysis blockers.
4. Run unit tests, then integration/feature tests.
5. Update Dockerfile, deploy image, and runtime extensions.
6. Smoke test health endpoint in the new container.

## Migration Output Template

- **From:** PHP 8.1 / Laravel 10
- **To:** PHP 8.3 / Laravel 11
- **Blockers:** `doctrine/annotations`, custom extension `redis` package pin
- **Verified:** `vendor/bin/phpunit`, `vendor/bin/phpstan`, CI green on branch
