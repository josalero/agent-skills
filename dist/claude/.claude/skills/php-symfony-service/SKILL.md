---
name: php-symfony-service
description: Build, review, refactor, and test Symfony backend services. Use when working on Symfony controllers, services, validation, serialization, Messenger, security, configuration, Doctrine integration, API Platform, or production service behavior.
---

# PHP Symfony Service

## Workflow

1. Inspect the PHP version, Symfony version, Flex structure, bundles in use, tests, and configuration style.
2. Identify whether the task is implementation, review, refactor, test coverage, migration, or production behavior.
3. Follow existing controller, service, repository, DTO, validator, serializer, and security patterns.
4. Keep API boundaries explicit: input DTOs, output DTOs, validation, problem responses, pagination, and compatibility.
5. Check authorization voters, transaction boundaries, Doctrine access patterns, Messenger handlers, and observability signals.
6. Verify with targeted unit or kernel tests first, then broader integration tests when behavior crosses layers.

## References

- Read `references/api-design.md` for controllers, DTOs, validation, serialization, and error responses.
- Read `references/services-and-testing.md` for dependency injection, Messenger, and WebTestCase patterns.

## Output

After changes, summarize:

- Files changed
- Behavior added or fixed
- Tests added and why each test type was chosen
- Commands to run (`bin/phpunit`, `symfony php bin/phpunit`, or narrower filters)
- Risks, migration notes, or API compatibility concerns
