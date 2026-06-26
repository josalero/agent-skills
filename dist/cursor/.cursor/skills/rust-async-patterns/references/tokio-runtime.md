# Tokio Runtime

## Multi-thread for Production Services

```rust
#[tokio::main]
async fn main() -> Result<()> {
    run_server().await
}
```

## spawn_blocking for CPU/Blocking Work

```rust
let data = tokio::task::spawn_blocking(move || expensive_parse(bytes))
    .await??;
```

## Timeouts

```rust
use tokio::time::{timeout, Duration};

timeout(Duration::from_secs(5), client.fetch(id)).await??
```

## Graceful Shutdown

Listen for SIGTERM/Ctrl+C, stop accepting, drain in-flight requests, then exit.
