# Eval: Rust Testing Verification

## Prompt

Add regression tests for a panic when optional discount code was None in apply_discount. Include unit tests and an Axum handler test if the function is exposed via HTTP.

## Expected Agent Behavior

- Reproduces failure with test when possible
- Covers None, empty, invalid inputs
- Uses appropriate unit vs integration test
- Runs cargo test on affected crate

## Failure Signals

- Only happy path tested
- Uses unwrap in tests without asserting error paths
- Ignores HTTP contract when endpoint exists
