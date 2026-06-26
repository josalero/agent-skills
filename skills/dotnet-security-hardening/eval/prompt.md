# Eval: .NET Security Hardening

## Prompt

Review this endpoint and harden it. The app uses ASP.NET Core 8 and EF Core. Users should only cancel their own orders.

```csharp
[HttpPost("{id:guid}/cancel")]
public async Task<IActionResult> Cancel(Guid id, [FromQuery] string userId)
{
    var order = await db.Orders.FindAsync(id);
    if (order is null) return NotFound();
    order.Status = OrderStatus.Cancelled;
    await db.SaveChangesAsync();
    return Ok();
}
```

JWT authentication is already configured; orders have an `OwnerId` column.

## Expected Agent Behavior

- Removes trust in client-supplied `userId` query parameter
- Adds `[Authorize]` and checks `OwnerId` against claims server-side
- Uses parameterized EF access (already OK) and safe NotFound without leaking existence to unauthorized users where appropriate
- Returns ProblemDetails or consistent error shape
- Suggests authorization test for owner vs non-owner
- Mentions not logging sensitive order data

## Failure Signals

- Keeps `userId` from query string as authorization source
- No `[Authorize]` on mutating endpoint
- Returns detailed exception messages to client
- Suggests storing JWT signing key in appsettings committed to git
