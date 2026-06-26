# Toolchain and Edition

## rust-toolchain.toml

```toml
[toolchain]
channel = "1.85.0"
components = ["rustfmt", "clippy"]
```

## Edition in Cargo.toml

```toml
[package]
edition = "2021"
rust-version = "1.75"
```

## Verification

```bash
cargo check --workspace
cargo test --workspace
cargo clippy --workspace -- -D warnings
```
