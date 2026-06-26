---
name: php-laravel-service
description: Build, review, refactor, and test Laravel backend services. Use when working on Laravel REST APIs, form requests, resources, policies, queues, events, configuration, transactions, observability, feature tests, or production service behavior.
---

# PHP Laravel Service

## Workflow

1. Inspect the PHP version, Laravel version, Composer constraints, app structure, tests, and configuration style.
2. Identify whether the task is implementation, review, refactor, test coverage, migration, or production behavior.
3. Follow existing controller, action/service, repository, request, resource, policy, and config patterns.
4. Keep API boundaries explicit: form requests, API resources, validation, error responses, pagination, and compatibility.
5. Check authorization policies, transaction boundaries, Eloquent access patterns, queue idempotency, and observability signals.
6. Verify with targeted unit or feature tests first, then broader integration tests when behavior crosses layers.

## References

- Read `references/api-design.md` for controllers, form requests, resources, pagination, and error responses.
- Read `references/testing-and-queues.md` for feature tests, fakes, jobs, and queue verification.

## Output

After changes, summarize:

- Files changed
- Behavior added or fixed
- Tests added and why each test type was chosen
- Commands to run (`php artisan test`, `vendor/bin/phpunit`, or narrower filters)
- Risks, migration notes, or API compatibility concerns
