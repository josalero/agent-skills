---
name: php-quality-gates
description: Configure and fix PHP CI quality gates for Laravel or Symfony projects. Use when setting up Composer quality scripts, PHPUnit in CI, PHPStan or Psalm levels, PHP-CS-Fixer, Rector, infection mutation testing gates, or fixing pipeline failures on static analysis and tests.
---

# PHP Quality Gates

## Workflow

1. Read `composer.json` scripts, `phpunit.xml`, PHPStan/Psalm config, and CI workflow.
2. Identify the project's **quality script** — e.g. `composer test`, `composer check`, `composer quality`.
3. Read `references/ci-pipeline-gates.md` for pipeline layout.
4. Read `references/static-analysis-and-style.md` for PHPStan, Psalm, CS Fixer, and Rector.
5. Fix test failures before lowering analysis levels; ratchet PHPStan level on new code when adopting gates.
6. Keep Laravel Pint vs PHP-CS-Fixer choice consistent with the repo — do not introduce duplicate formatters.
7. Run the same Composer script locally that CI runs.

## Gate Checklist

- PHPUnit passes in CI with same PHP version as production target.
- Static analysis (PHPStan or Psalm) runs at agreed level — not skipped in CI.
- Code style enforced via Pint, PHP-CS-Fixer, or PHPCS — verify step in CI.
- Composer `--no-dev` production builds separate from quality gates on dev dependencies.
- `.env` and secrets not required for CI unit tests (use `.env.testing` or mocks).

## Output

Summarize gates, Composer/CI commands, config files touched, verification steps, deferred baselines.

## Related Skills

- `php-testing-verification` — PHPUnit patterns
- `testing-strategy` — gate policy
- `php-laravel-service` / `php-symfony-service` — application fixes
