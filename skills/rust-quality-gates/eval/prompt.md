# Eval: Rust Quality Gates

## Prompt

Enable clippy -D warnings and rustfmt --check in CI for our Cargo workspace. Fix violations in the auth crate without allowing warnings at crate root.

## Expected Agent Behavior

- Updates CI workflow with clippy and fmt steps
- Fixes or narrowly allows specific lints with comment
- Runs cargo test and clippy locally
- Keeps workspace building on pinned toolchain

## Failure Signals

- #![allow(warnings)] at crate root
- Removes clippy from CI after failures
- Toolchain mismatch between local and CI
