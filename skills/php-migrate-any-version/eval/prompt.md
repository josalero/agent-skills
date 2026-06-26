# Eval: PHP Migrate Any Version

## Prompt

Migrate this project from PHP 8.1 to PHP 8.3. Update Composer platform requirements, CI workflow, and Docker base image. Identify source or dependency blockers. Run tests incrementally.

Current hints:

- `composer.json` requires `"php": "^8.1"`
- CI uses `php-version: '8.1'`
- Dockerfile uses `php:8.1-fpm`
- One package fails on 8.3 with dynamic property deprecation warnings promoted to exceptions in tests

## Expected Agent Behavior

- Reads migration path references before editing
- Updates Composer/CI/container config first, then dependencies, then source
- Proposes focused test and PHPStan commands after each step
- Replaces dynamic property usage with typed properties or readonly DTOs
- Summarizes versions changed, blockers, and remaining follow-ups
- Does not combine unrelated framework major upgrades in the same change unless requested

## Failure Signals

- Changes source before Composer resolves on 8.3
- Updates PHP in only one of Composer, CI, and Docker
- Skips test verification between steps
- Suppresses deprecations globally instead of fixing root cause
- Removes failing tests instead of fixing compatibility
