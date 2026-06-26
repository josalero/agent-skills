# Profiling and Metrics

## flamegraph

```bash
cargo flamegraph --bin api-server
```

## tracing Spans

Instrument handler and repository spans with consistent names for latency breakdown.

## Benchmarks

Use `criterion` for micro-benchmarks of hot algorithms — not a substitute for load tests.

## Production Signals

| Metric | May indicate |
| --- | --- |
| p99 latency up | lock contention, slow queries, GC in JNI deps |
| RSS growth | unbounded caches, channel backlog |
| CPU high | serde on large payloads, regex catastrophes |
