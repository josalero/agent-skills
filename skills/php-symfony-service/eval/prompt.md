# Eval: PHP Symfony Service

## Prompt

Add a POST `/api/v1/orders` endpoint that accepts `sku` and `quantity`, validates input, persists an order, and returns `201` with order id and status. Follow existing project patterns. Include WebTestCase and service unit tests.

Existing stack: Symfony 7, Doctrine ORM, Validator, PHPUnit, MapRequestPayload.

## Expected Agent Behavior

- Inspects `config/routes`, existing controllers, DTOs, services, and tests first
- Uses validated input DTOs and response DTOs instead of returning entities directly
- Places persistence in a service with explicit transaction boundary
- Adds WebTestCase for HTTP contract and unit test for service rules
- Summarizes files changed, tests added, and `bin/phpunit --filter=...` command

## Failure Signals

- Returns Doctrine entity JSON from controller without serializer groups or DTO mapping
- No validation on request payload
- Uses full kernel tests only when WebTestCase or unit tests suffice
- Missing test for invalid quantity or blank sku
- Authorization omitted on a protected route
