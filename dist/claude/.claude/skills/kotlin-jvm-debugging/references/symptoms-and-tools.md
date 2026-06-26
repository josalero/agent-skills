# Symptoms and Tools

| Symptom | First evidence to collect |
| --- | --- |
| Memory growth | Heap histogram, GC logs, leak suspect report |
| Latency spikes | Traces, thread dumps during spike, pool metrics |
| CPU high | Async profiler, flame graph, hot method list |
| Blocked threads | Thread dump, lock analysis |
| Coroutine leaks | Structured concurrency audit, active job metrics |

## Safe Collection

```bash
jcmd <pid> GC.heap_info
jcmd <pid> Thread.print
```

Coordinate with ops before heap dumps in production.
