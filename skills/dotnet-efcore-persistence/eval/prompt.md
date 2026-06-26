# Eval: .NET EF Core Persistence

## Prompt

The GET `/api/v1/orders` endpoint is slow. Logs show 1 query for orders and then N queries for `LineItems`. Fix the N+1 without loading unnecessary columns. The project uses EF Core 8 with PostgreSQL.

Existing code pattern:

```csharp
var orders = await db.Orders
    .OrderByDescending(o => o.CreatedAt)
    .Take(20)
    .ToListAsync(cancellationToken);
// API response maps order.LineItems.Count per order
```

## Expected Agent Behavior

- Enables or references SQL logging to confirm N+1
- Replaces naive load with projection or controlled `Include`/`AsSplitQuery`
- Uses `AsNoTracking()` for read-only list
- Does not load full `LineItem` entities when only count is needed
- Adds or updates integration test asserting acceptable query behavior where feasible
- Summarizes evidence, fix, and verification command

## Failure Signals

- Adds blanket `.Include(o => o.LineItems)` on all endpoints without measuring need
- Loads all columns when DTO needs count only
- Fixes in the controller instead of repository/query layer
- No mention of query count before/after
