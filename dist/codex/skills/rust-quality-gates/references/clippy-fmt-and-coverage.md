# Clippy, Format, and Coverage

## Workspace Clippy Config

```toml
[lints.clippy]
all = "warn"
pedantic = "warn"
```

## rustfmt

Add `rustfmt.toml` at workspace root; enforce in CI with `--check`.

## llvm-cov

```bash
cargo llvm-cov --workspace --lcov --output-path lcov.info
```

Set thresholds in CI or coverage upload tool — exclude benches and build scripts.
