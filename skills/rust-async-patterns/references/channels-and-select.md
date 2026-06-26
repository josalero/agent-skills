# Channels and select!

## mpsc for Worker Pipelines

```rust
let (tx, mut rx) = tokio::sync::mpsc::channel(32);
tokio::spawn(async move {
    while let Some(job) = rx.recv().await {
        process(job).await;
    }
});
```

## select! for Multiplexing

```rust
tokio::select! {
    result = operation() => result?,
    _ = shutdown.cancelled() => break,
}
```

## Backpressure

Size channels intentionally. Unbounded channels hide overload until OOM.
