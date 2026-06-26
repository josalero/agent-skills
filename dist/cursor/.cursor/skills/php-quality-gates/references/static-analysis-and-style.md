# PHP Static Analysis and Style

## PHPStan

```neon
# phpstan.neon
parameters:
    level: 8
    paths:
        - app
        - src
    excludePaths:
        - tests/bootstrap.php
```

Raise level incrementally; use baseline (`phpstan-baseline.neon`) for legacy debt with cleanup plan.

```bash
vendor/bin/phpstan analyse --memory-limit=1G
```

## Psalm

Alternative or complement — do not run both at max strictness without team agreement.

```xml
<!-- psalm.xml -->
<issueHandlers>
    <MissingParamType errorLevel="error"/>
</issueHandlers>
```

## PHP-CS-Fixer / Laravel Pint

**PHP-CS-Fixer:**

```bash
vendor/bin/php-cs-fixer fix --dry-run --diff
```

**Laravel Pint:**

```bash
./vendor/bin/pint --test
```

CI must use `--test` / `--dry-run` — not auto-commit in pipeline.

## Rector (optional gate)

Use in dedicated job or weekly — can be slow on PR. Prefer `rector --dry-run` in CI when adopted.

## PHPUnit Coverage

```xml
<!-- phpunit.xml -->
<coverage>
    <report>
        <clover outputFile="build/coverage.xml"/>
    </report>
</coverage>
```

Enforce minimum on `src/` namespaces with business logic — exclude migrations and config when noisy.

## Infection (mutation testing)

Advisory or nightly initially — mutation score is expensive. Do not block all PRs until suite is fast enough.

## Fixing Failures

1. Prefer fixing types and nullability over `@phpstan-ignore` comments.
2. Suppressions require short justification comment and ticket.
3. Distinguish framework false positives (document in config) from real bugs.

## Related Skills

- `php-testing-verification` — meaningful PHPUnit tests
- `php-security-hardening` — security-sensitive paths deserve higher analysis level
