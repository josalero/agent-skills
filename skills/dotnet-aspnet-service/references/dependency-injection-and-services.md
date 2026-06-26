# Dependency Injection and Services

## Service Registration

```csharp
// Program.cs or ServiceCollectionExtensions.cs
public static class OrderServiceExtensions
{
    public static IServiceCollection AddOrderServices(this IServiceCollection services)
    {
        services.AddScoped<IOrderRepository, EfOrderRepository>();
        services.AddScoped<IOrderService, OrderService>();
        return services;
    }
}
```

| Lifetime | Use for |
| --- | --- |
| Singleton | Stateless caches, options, `HttpClient` factory config |
| Scoped | DbContext, unit-of-work, request-scoped services |
| Transient | Lightweight stateless helpers (use sparingly) |

Never inject `DbContext` into singletons.

## Service Layer Pattern

```csharp
public interface IOrderService
{
    Task<OrderResponse> CreateAsync(CreateOrderRequest request, CancellationToken cancellationToken);
    Task<OrderResponse> GetAsync(Guid id, CancellationToken cancellationToken);
}

public sealed class OrderService(IOrderRepository repository, IClock clock) : IOrderService
{
    public async Task<OrderResponse> CreateAsync(
        CreateOrderRequest request,
        CancellationToken cancellationToken)
    {
        var order = Order.Create(request.Sku, request.Quantity, clock.UtcNow);
        await repository.AddAsync(order, cancellationToken);
        return OrderMapper.ToResponse(order);
    }

    public async Task<OrderResponse> GetAsync(Guid id, CancellationToken cancellationToken)
    {
        var order = await repository.FindByIdAsync(id, cancellationToken)
            ?? throw new OrderNotFoundException(id);
        return OrderMapper.ToResponse(order);
    }
}
```

Keep HTTP concerns out of services — no `IResult`, `ProblemDetails`, or status codes in domain/service code.

## Options and Configuration

```csharp
public sealed class OrderOptions
{
    public const string SectionName = "Orders";
    public int MaxQuantity { get; init; } = 1000;
}

// Program.cs
builder.Services.Configure<OrderOptions>(
    builder.Configuration.GetSection(OrderOptions.SectionName));

// Service
public sealed class OrderValidator(IOptions<OrderOptions> options)
{
    public void ValidateQuantity(int quantity)
    {
        if (quantity > options.Value.MaxQuantity)
            throw new ValidationException($"Quantity cannot exceed {options.Value.MaxQuantity}.");
    }
}
```

Bind configuration to strongly typed options; validate with `ValidateOnStart()` for critical settings.

## Middleware Ordering

Typical pipeline order:

```csharp
app.UseExceptionHandler();
app.UseHttpsRedirection();
app.UseAuthentication();
app.UseAuthorization();
app.MapControllers(); // or MapGroup for Minimal APIs
```

Exception handling and ProblemDetails registration belong early; auth before endpoints that require it.

## Testing Services

```csharp
public sealed class OrderServiceTests
{
    [Fact]
    public async Task CreateAsync_returns_response_with_id()
    {
        var repository = Substitute.For<IOrderRepository>();
        var clock = Substitute.For<IClock>();
        clock.UtcNow.Returns(DateTimeOffset.UtcNow);

        var service = new OrderService(repository, clock);
        var response = await service.CreateAsync(
            new CreateOrderRequest { Sku = "SKU-1", Quantity = 2 },
            CancellationToken.None);

        Assert.NotEqual(Guid.Empty, response.Id);
        await repository.Received(1).AddAsync(Arg.Any<Order>(), Arg.Any<CancellationToken>());
    }
}
```

Prefer unit tests for business rules; use `WebApplicationFactory` when routing, binding, or ProblemDetails mapping must be verified.
