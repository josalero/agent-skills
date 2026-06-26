---
name: rust-migrate-any-version
description: Plan and execute Rust edition and toolchain migrations. Use when upgrading Rust edition (2018→2021→2024), MSRV, rust-toolchain.toml, breaking dependency majors, or fixing compile errors after a rustc bump.
---

# Rust Migrate Any Version

## Workflow

1. Record current edition, MSRV, `rust-toolchain.toml`, and key dependency versions from `Cargo.toml`/`Cargo.lock`.
2. Read edition guide and dependency changelogs for the target version.
3. Produce a phased plan: toolchain bump, edition fixits, dependency alignment, compile fixes, test verification, CI update.
4. Run `cargo fix --edition` where appropriate; review diffs — do not blindly accept.
5. Run full `cargo test`, `cargo clippy`, and workspace builds.
6. Update CI rustup channel and document developer setup.

## References

- Read `references/migration-planning.md` for phased rollout, risk assessment, and rollback strategy.
- Read `references/toolchain-and-edition.md` for rust-toolchain.toml, edition flags, and MSRV policy.

## Migration Checklist

- Edition, MSRV, and dependency versions are compatible.
- `cargo fix` changes reviewed for behavior impact.
- All workspace crates compile and test.
- CI pins the same toolchain as local.
- Rollback path documented.

## Output

Summarize current and target versions, phased plan, files changed, verification commands, known risks, and rollback steps.
