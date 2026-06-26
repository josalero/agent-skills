# Eval: Rust Core Engineering

## Prompt

Refactor the discount function to use typed LineItem structs, proper error handling for invalid input, and Decimal for money math. Preserve behavior and add unit tests for edge cases.

## Expected Agent Behavior

- Introduces newtypes or structs instead of tuples
- Avoids unwrap in library code
- Adds regression tests
- Runs cargo test on affected crate

## Failure Signals

- Uses f64 for money without justification
- Panics on invalid input in public API
- Refactors without tests
