# Migrations and Transactions

## Adding Migrations

```bash
dotnet ef migrations add AddOrderStatusIndex --project src/Infrastructure --startup-project src/Api
dotnet ef database update --project src/Infrastructure --startup-project src/Api
```

Review generated SQL before applying to production:

```bash
dotnet ef migrations script --idempotent --output migrate.sql
```

## Index in Migration

```csharp
public partial class AddOrderStatusIndex : Migration
{
    protected override void Up(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.CreateIndex(
            name: "IX_Orders_Status_CreatedAt",
            table: "Orders",
            columns: new[] { "Status", "CreatedAt" });
    }

    protected override void Down(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.DropIndex(name: "IX_Orders_Status_CreatedAt", table: "Orders");
    }
}
```

## Transaction Boundaries

```csharp
public async Task<OrderResponse> PlaceOrderAsync(
    PlaceOrderRequest request,
    CancellationToken cancellationToken)
{
    await using var transaction = await db.Database.BeginTransactionAsync(cancellationToken);
    try
    {
        var order = Order.Create(request);
        db.Orders.Add(order);
        await db.SaveChangesAsync(cancellationToken);

        await inventory.ReserveAsync(order.LineItems, cancellationToken);
        await db.SaveChangesAsync(cancellationToken);

        await transaction.CommitAsync(cancellationToken);
        return OrderMapper.ToResponse(order);
    }
    catch
    {
        await transaction.RollbackAsync(cancellationToken);
        throw;
    }
}
```

Prefer one `SaveChangesAsync` per logical unit when possible; use explicit transactions when coordinating multiple aggregates or external calls that must roll back together.

## Batch Writes

```csharp
public async Task ImportLineItemsAsync(
    IReadOnlyList<LineItem> items,
    CancellationToken cancellationToken)
{
    db.ChangeTracker.AutoDetectChangesEnabled = false;
    await db.LineItems.AddRangeAsync(items, cancellationToken);
    await db.SaveChangesAsync(cancellationToken);
    db.ChangeTracker.AutoDetectChangesEnabled = true;
}
```

For large imports, consider `ExecuteUpdate` / `ExecuteDelete` (EF Core 7+) to avoid loading entities:

```csharp
await db.Orders
    .Where(o => o.Status == OrderStatus.Draft && o.CreatedAt < cutoff)
    .ExecuteDeleteAsync(cancellationToken);
```

## DbContext Lifetime

Register `DbContext` as scoped — one instance per request:

```csharp
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseNpgsql(builder.Configuration.GetConnectionString("Default")));
```

Never share a scoped context across concurrent tasks.

## Migration Checklist

- Migrations are committed with the model change in the same PR
- Destructive changes (drop column, change type) have backfill or multi-step plan
- Production deploy runs migrations before or during rollout with rollback strategy documented
- Seed data uses `HasData` or idempotent scripts — not manual prod edits
