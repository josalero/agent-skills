---
name: rust-quality-gates
description: Configure and fix Rust CI quality gates for Cargo workspaces. Use when setting up or repairing cargo test, clippy -D warnings, rustfmt --check, cargo deny, llvm-cov coverage thresholds, or PR pipeline failures.
---

# Rust Quality Gates

## Workflow

1. Read `Cargo.toml` workspace config, `rust-toolchain.toml`, clippy lints, and CI workflow.
2. Map the **canonical gate command** — typically `cargo test --workspace`, `cargo clippy --workspace -- -D warnings`, `cargo fmt --check`.
3. Classify failures: compile, test, clippy, fmt, deny, coverage — fix in that order.
4. Read `references/ci-pipeline-gates.md` for pipeline staging.
5. Read `references/clippy-fmt-and-coverage.md` for lint, format, and coverage configuration.
6. Prefer fail-the-build on new warnings; allow `#![allow]` only with narrow rationale.
7. Align local commands with CI rustup channel.

## Gate Checklist

- `cargo test --workspace` passes on PR.
- `cargo clippy --workspace -- -D warnings` passes when enforced.
- `cargo fmt --check` passes when formatting is enforced.
- `cargo deny` or audit step runs for advisories when configured.
- Coverage thresholds apply to meaningful crates, not generated code.
- CI uses the same toolchain as `rust-toolchain.toml`.

## Output

Summarize gates, CI commands, files changed, local verification commands, and deferred baseline work.

## Related Skills

- `rust-testing-verification` — test design
- `testing-strategy` — cross-stack gate policy
- `rust-core-engineering` — code fixes behind failures
