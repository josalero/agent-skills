# Eval: .NET Runtime Diagnostics

## Prompt

Production alert: p99 latency on order placement jumped from 200ms to 8s after last deploy. CPU is low, memory stable, no errors in logs. The team suspects GC tuning. Investigate and propose the most likely fix.

Recent code change added:

```csharp
public OrderResponse PlaceOrder(PlaceOrderRequest request)
{
    return _orderService.PlaceOrderAsync(request).Result;
}
```

## Expected Agent Behavior

- Identifies sync-over-async / thread pool starvation as primary hypothesis before GC changes
- References `dotnet-counters` (thread-pool queue) or traces as evidence to collect
- Recommends converting to async end-to-end, not arbitrary `DOTNET_ThreadPool_*` tuning
- Mentions verifying with traces and latency metrics after fix
- Documents rollback if a config change is attempted

## Failure Signals

- Jumps to Server GC / heap limit changes without evidence
- Ignores `.Result` in the diff
- Suggests restart-only mitigation with no root cause
- No verification metric named
