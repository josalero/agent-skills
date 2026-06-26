# CI Pipeline Gates for Rust

## Typical PR Job

```yaml
- run: rustup show
- run: cargo test --workspace --all-features
- run: cargo clippy --workspace --all-targets -- -D warnings
- run: cargo fmt --all -- --check
```

## Caching

Cache `~/.cargo/registry`, `~/.cargo/git`, and `target/` keyed on lockfile hash.

## MSRV Job

Optional separate job: `cargo +1.75.0 check --workspace` when MSRV is policy.
