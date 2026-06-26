# Rust Migration Planning

## Phase 1 — Inventory

- `edition` in each crate `Cargo.toml`
- `rust-version` MSRV field
- `rust-toolchain.toml` channel
- Breaking majors in `Cargo.lock`

## Phase 2 — Upgrade Order

1. Bump toolchain in branch
2. Run edition fixits per crate
3. Update breaking dependencies incrementally
4. `cargo test --workspace`
5. Update CI rustup component

## Risk Areas

- Async trait/object changes across editions
- `sqlx`/`tokio` major version API shifts
- Proc-macro crate compatibility

## Rollback

Tag pre-migration commit; revert toolchain file and lockfile together.
