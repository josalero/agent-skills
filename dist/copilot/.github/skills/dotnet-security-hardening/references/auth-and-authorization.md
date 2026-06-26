# Authentication and Authorization

## JWT Bearer Authentication

```csharp
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.MapInboundClaims = false;
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuer = true,
            ValidIssuer = builder.Configuration["Auth:Issuer"],
            ValidateAudience = true,
            ValidAudience = builder.Configuration["Auth:Audience"],
            ValidateLifetime = true,
            ValidateIssuerSigningKey = true,
            IssuerSigningKey = new SymmetricSecurityKey(
                Encoding.UTF8.GetBytes(builder.Configuration["Auth:SigningKey"]!)),
            ClockSkew = TimeSpan.FromMinutes(1)
        };
    });

builder.Services.AddAuthorization(options =>
{
    options.AddPolicy("OrdersWrite", policy =>
        policy.RequireAuthenticatedUser()
              .RequireClaim("scope", "orders:write"));

    options.AddPolicy("AdminOnly", policy =>
        policy.RequireRole("Admin"));
});
```

Signing keys come from configuration or Key Vault — never hardcoded in source.

## Protecting Endpoints

```csharp
app.MapPost("/api/v1/orders", async (...) => { /* ... */ })
   .RequireAuthorization("OrdersWrite");

[Authorize(Policy = "AdminOnly")]
[HttpDelete("{id:guid}")]
public async Task<IActionResult> Delete(Guid id, CancellationToken cancellationToken)
{
    await orderService.DeleteAsync(id, cancellationToken);
    return NoContent();
}
```

Default deny for sensitive Minimal API groups:

```csharp
var orders = app.MapGroup("/api/v1/orders").RequireAuthorization();
orders.MapGet("/", ListOrders);
orders.MapPost("/", CreateOrder);
```

## Resource-Based Authorization

```csharp
public sealed class OrderOwnerRequirement : IAuthorizationRequirement { }

public sealed class OrderOwnerHandler(
    AppDbContext db,
    IHttpContextAccessor httpContextAccessor) : AuthorizationHandler<OrderOwnerRequirement, Guid>
{
    protected override async Task HandleRequirementAsync(
        AuthorizationHandlerContext context,
        OrderOwnerRequirement requirement,
        Guid orderId)
    {
        var userId = context.User.FindFirstValue(ClaimTypes.NameIdentifier);
        if (userId is null) return;

        var ownsOrder = await db.Orders.AnyAsync(o => o.Id == orderId && o.OwnerId == userId);
        if (ownsOrder)
            context.Succeed(requirement);
    }
}

// Usage
await authorizationService.AuthorizeAsync(user, orderId, "OrderOwner");
```

Check ownership on the server — never trust client-supplied user id alone.

## HTTPS and Headers

```csharp
if (!app.Environment.IsDevelopment())
{
    app.UseHsts();
    app.UseHttpsRedirection();
}

app.Use(async (context, next) =>
{
    context.Response.Headers.TryAdd("X-Content-Type-Options", "nosniff");
    context.Response.Headers.TryAdd("X-Frame-Options", "DENY");
    await next();
});
```

## Auth Review Checklist

- `[AllowAnonymous]` only on truly public endpoints
- Token lifetime and refresh strategy documented
- CORS policy is explicit — no `AllowAnyOrigin` with credentials
- Admin and internal endpoints not exposed on public ingress without additional controls
