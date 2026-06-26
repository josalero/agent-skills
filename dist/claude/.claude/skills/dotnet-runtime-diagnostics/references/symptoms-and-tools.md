# Symptoms and Tools

## Symptom → First Tool

| Symptom | Start with |
| --- | --- |
| Rising memory | `dotnet-counters`, then dump if leak suspected |
| Latency spikes | Traces + `http.server.request.duration`, thread-pool counters |
| High CPU | `dotnet-trace` with CPU sample provider |
| Request hangs | Thread pool queue, sync-over-async search, DB pool waits |
| Startup slow | Startup trace, configuration binding, JIT/ReadyToRun |

## dotnet-counters (Live Metrics)

```bash
# List available counters for a running app
dotnet-counters list --runtime

# Monitor key ASP.NET Core and runtime counters
dotnet-counters monitor --process-id <pid> \
  System.Runtime \
  Microsoft.AspNetCore.Hosting \
  Microsoft-AspNetCore-Server-Kestrel \
  System.Net.Http
```

Watch for:

- `threadpool-thread-count` and `threadpool-queue-length` — starvation signal
- `gc-heap-size` and `gen-2-gc-count` — memory pressure
- `current-requests` and `requests-per-second` — load correlation

## dotnet-trace

```bash
dotnet-trace collect --process-id <pid> --profile cpu-sampling --duration 00:00:30
```

Open the `.nettrace` file in PerfView or Visual Studio to find hot methods.

## Structured Logs

Correlate by `TraceId` / `SpanId` when OpenTelemetry is enabled:

```csharp
builder.Services.AddOpenTelemetry()
    .WithTracing(tracing => tracing
        .AddAspNetCoreInstrumentation()
        .AddHttpClientInstrumentation()
        .AddEntityFrameworkCoreInstrumentation());
```

Search logs for the slow request's trace id before changing GC flags.

## Thread Pool Starvation Signal

Symptoms: latency grows under load, `ThreadPool` queue length rises, minimal CPU.

Common causes in ASP.NET Core:

- `.Result` / `.Wait()` on async paths
- `Task.Run` wrapping synchronous I/O
- Blocking calls inside lock in request path

Fix the blocking pattern — do not raise `MinThreads` without evidence and a rollback plan.

## Safe Collection Checklist

- Prefer read-only tooling in production (`dotnet-counters`, traces with short duration)
- Coordinate dump collection with ops — dumps can pause the process briefly
- Record PID, instance, deploy version, and time window with every artifact
