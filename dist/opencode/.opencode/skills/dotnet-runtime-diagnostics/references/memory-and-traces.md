# Memory and Traces

## GC and Heap Growth

Monitor over time — a single snapshot is not enough:

```bash
dotnet-counters monitor --process-id <pid> System.Runtime --counters gc-heap-size,gen-0-gc-count,gen-1-gc-count,gen-2-gc-count,alloc-rate
```

Interpretation:

- Steadily rising `gc-heap-size` after GC with flat traffic → possible leak
- Frequent gen-2 collections with high allocation rate → allocation-heavy hot path
- Large object heap pressure → review buffers, strings, and caching

## Collecting a Dump

```bash
dotnet-dump collect --process-id <pid> --type Full
dotnet-dump analyze core_*.dump
```

In the SOS REPL:

```
dumpheap -stat
dumpheap -type MyApp.OrderCache -min 85000
gcroot <object_address>
```

Look for static caches, event handlers, or `DbContext` held beyond request scope.

## Common Leak Patterns in .NET Services

```csharp
// Leak — static cache without eviction
public static class OrderCache
{
    public static readonly ConcurrentDictionary<Guid, Order> Entries = new();
}

// Fix — bounded cache with expiration
builder.Services.AddMemoryCache();
// or IMemoryCache with size limits and sliding expiration
```

```csharp
// Leak — DbContext captured in singleton
public sealed class ReportGenerator(AppDbContext db) // wrong lifetime
{
    // ...
}

// Fix — inject IDbContextFactory<AppDbContext> or scoped service
```

## Distributed Trace Analysis

For slow HTTP requests, inspect span waterfall:

1. Kestrel receive → middleware → controller/action
2. EF Core `SaveChanges` / query spans
3. Outbound `HttpClient` calls

If total time is dominated by a single EF query, fix the query — not GC.

Example custom span for business operations:

```csharp
public async Task ProcessOrderAsync(Guid orderId, CancellationToken cancellationToken)
{
    using var activity = ActivitySource.StartActivity("ProcessOrder");
    activity?.SetTag("order.id", orderId.ToString());

    await _pipeline.RunAsync(orderId, cancellationToken);
}
```

## Latency Investigation Workflow

1. Identify p95/p99 regression window from metrics
2. Pull exemplar traces from that window
3. Compare to baseline period with similar traffic
4. Check deploy diff, feature flags, and downstream dependency latency
5. Reproduce under load in staging with the same trace instrumentation

## Recovery Verification

After a fix, confirm:

- Same `dotnet-counters` metrics return to baseline under comparable load
- Trace p95 for affected endpoint drops
- No new errors in logs or health checks

Document the before/after metric values in the incident summary.
