# Eval: Rust Migrate Any Version

## Prompt

Plan and execute migrating our workspace from edition 2018 to 2021 with MSRV 1.75. Several crates use async-trait and sqlx 0.6. CI must stay green.

## Expected Agent Behavior

- Phased plan before edits
- Runs cargo fix with review
- Aligns sqlx and async ecosystem versions
- Updates CI rust-toolchain
- Documents rollback

## Failure Signals

- Jumps edition without testing all crates
- MSRV lower than dependency requirements
- Skips clippy after migration
