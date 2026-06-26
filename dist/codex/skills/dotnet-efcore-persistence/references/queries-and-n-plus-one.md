# Queries and N+1

## Detect N+1

Enable sensitive logging in development:

```csharp
optionsBuilder
    .UseNpgsql(connectionString)
    .LogTo(Console.WriteLine, LogLevel.Information)
    .EnableSensitiveDataLogging(); // dev only
```

Symptom: one query for the parent list, then one query per child when the view accesses a navigation property.

## Projection Instead of Full Entities

```csharp
// Avoid — loads Order + lazy-loads LineItems per order in the view
public async Task<List<Order>> ListRecentAsync(CancellationToken cancellationToken) =>
    await db.Orders
        .OrderByDescending(o => o.CreatedAt)
        .Take(20)
        .ToListAsync(cancellationToken);

// Prefer — single query with projection
public async Task<List<OrderSummaryDto>> ListRecentAsync(CancellationToken cancellationToken) =>
    await db.Orders
        .OrderByDescending(o => o.CreatedAt)
        .Take(20)
        .Select(o => new OrderSummaryDto(
            o.Id,
            o.Status,
            o.LineItems.Count,
            o.Total))
        .ToListAsync(cancellationToken);
```

## Explicit Include and Split Queries

```csharp
public async Task<OrderDetailDto?> GetDetailAsync(Guid id, CancellationToken cancellationToken) =>
    await db.Orders
        .AsSplitQuery() // avoids cartesian explosion on multiple collections
        .Include(o => o.LineItems)
        .Include(o => o.Shipments)
        .Where(o => o.Id == id)
        .Select(o => new OrderDetailDto(
            o.Id,
            o.Status,
            o.LineItems.Select(li => new LineItemDto(li.Sku, li.Quantity)).ToList(),
            o.Shipments.Select(s => new ShipmentDto(s.TrackingNumber, s.ShippedAt)).ToList()))
        .FirstOrDefaultAsync(cancellationToken);
```

Use `AsSplitQuery()` when including multiple collections; use `AsNoTracking()` for read-only endpoints.

## Compiled Queries for Hot Paths

```csharp
private static readonly Func<AppDbContext, Guid, Task<Order?>> FindOrderById =
    EF.CompileAsyncQuery((AppDbContext db, Guid id) =>
        db.Orders.FirstOrDefault(o => o.Id == id));

public Task<Order?> FindByIdAsync(Guid id, CancellationToken cancellationToken) =>
    FindOrderById(db, id);
```

## Pagination at the Database

```csharp
public async Task<PagedResult<OrderSummaryDto>> ListAsync(
    int page,
    int size,
    CancellationToken cancellationToken)
{
    var query = db.Orders.AsNoTracking().OrderByDescending(o => o.CreatedAt);

    var total = await query.CountAsync(cancellationToken);
    var items = await query
        .Skip(page * size)
        .Take(size)
        .Select(o => new OrderSummaryDto(o.Id, o.Status, o.CreatedAt))
        .ToListAsync(cancellationToken);

    return new PagedResult<OrderSummaryDto>(items, page, size, total);
}
```

Never `ToListAsync()` then `Skip`/`Take` in memory on large tables.

## Query Review Checklist

- Count SQL statements per HTTP request for list/detail endpoints
- Filter and sort columns have supporting indexes
- `AsNoTracking()` on read-only queries
- No sync `ToList()` on IQueryable in async code paths
