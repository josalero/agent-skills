# Eval: Kotlin Testing Verification

## Prompt

Add regression tests for a bug where null discount codes caused NPE in DiscountService. Include unit tests for edge cases and a Spring slice test if the service is wired through a controller.

## Expected Agent Behavior

- Reproduces bug with failing test first when possible
- Covers null, empty, and invalid inputs
- Chooses unit vs slice test appropriately
- Runs narrowest ./gradlew test target

## Failure Signals

- Tests only happy path
- Uses Thread.sleep in coroutine tests
- No assertion on observable behavior
