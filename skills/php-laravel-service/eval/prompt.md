# Eval: PHP Laravel Service

## Prompt

Add a POST `/api/v1/orders` endpoint that accepts `sku` and `quantity`, validates input, persists an order, and returns `201` with order id and status. Follow existing project patterns. Include feature and service tests.

Existing stack: Laravel 11, Sanctum auth, PHPUnit, Eloquent.

## Expected Agent Behavior

- Inspects `routes/`, existing controllers, form requests, resources, and tests first
- Uses form request validation and API resources instead of returning models directly
- Places business logic in a service or action with `DB::transaction` when persistence spans writes
- Adds feature test for HTTP contract and unit test for service rules
- Summarizes files changed, tests added, and `php artisan test --filter=...` command

## Failure Signals

- Returns Eloquent model JSON from controller without resource shaping
- No validation on request body
- Uses full application bootstrap tests only when feature tests suffice
- Missing test for invalid quantity or blank sku
- Authorization omitted on a protected route
