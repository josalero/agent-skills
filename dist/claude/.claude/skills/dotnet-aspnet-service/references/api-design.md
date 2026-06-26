# ASP.NET Core API Design

Use explicit request and response types rather than exposing EF entities or domain internals.

## Minimal API With DTO Boundaries

```csharp
app.MapPost("/api/v1/orders", async (
    CreateOrderRequest request,
    IOrderService orderService,
    CancellationToken cancellationToken) =>
{
    var response = await orderService.CreateAsync(request, cancellationToken);
    return Results.Created($"/api/v1/orders/{response.Id}", response);
})
.WithName("CreateOrder")
.Produces<OrderResponse>(StatusCodes.Status201Created)
.ProducesValidationProblem();
```

## Controller With Validation

```csharp
[ApiController]
[Route("api/v1/orders")]
public sealed class OrdersController(IOrderService orderService) : ControllerBase
{
    [HttpPost]
    [ProducesResponseType(typeof(OrderResponse), StatusCodes.Status201Created)]
    [ProducesResponseType(typeof(ValidationProblemDetails), StatusCodes.Status400BadRequest)]
    public async Task<ActionResult<OrderResponse>> Create(
        [FromBody] CreateOrderRequest request,
        CancellationToken cancellationToken)
    {
        var response = await orderService.CreateAsync(request, cancellationToken);
        return CreatedAtAction(nameof(GetById), new { id = response.Id }, response);
    }

    [HttpGet]
    public async Task<PagedResult<OrderSummaryResponse>> List(
        [FromQuery] int page = 0,
        [FromQuery][Range(1, 100)] int size = 20,
        [FromQuery] OrderStatus? status = null,
        CancellationToken cancellationToken = default) =>
        await orderService.ListAsync(page, size, status, cancellationToken);
}
```

## Request Validation

```csharp
public sealed record CreateOrderRequest
{
    [Required]
    [MaxLength(64)]
    public required string Sku { get; init; }

    [Range(1, 1000)]
    public int Quantity { get; init; }
}
```

## ProblemDetails Exception Handler

```csharp
public sealed class OrderNotFoundException(Guid orderId) : Exception($"Order {orderId} was not found.")
{
    public Guid OrderId { get; } = orderId;
}

public sealed class GlobalExceptionHandler(ILogger<GlobalExceptionHandler> logger) : IExceptionHandler
{
    public async ValueTask<bool> TryHandleAsync(
        HttpContext httpContext,
        Exception exception,
        CancellationToken cancellationToken)
    {
        var (status, title, detail) = exception switch
        {
            OrderNotFoundException ex => (StatusCodes.Status404NotFound, "Order Not Found", ex.Message),
            ValidationException ex => (StatusCodes.Status400BadRequest, "Validation Failed", ex.Message),
            _ => (StatusCodes.Status500InternalServerError, "Server Error", "An unexpected error occurred.")
        };

        if (status >= 500)
            logger.LogError(exception, "Unhandled exception");

        var problem = new ProblemDetails
        {
            Status = status,
            Title = title,
            Detail = detail,
            Instance = httpContext.Request.Path
        };

        if (exception is OrderNotFoundException notFound)
            problem.Extensions["orderId"] = notFound.OrderId;

        httpContext.Response.StatusCode = status;
        await httpContext.Response.WriteAsJsonAsync(problem, cancellationToken);
        return true;
    }
}
```

Register in `Program.cs`:

```csharp
builder.Services.AddExceptionHandler<GlobalExceptionHandler>();
builder.Services.AddProblemDetails();
// ...
app.UseExceptionHandler();
```

## API Review Checklist

- Validation at the boundary; never trust client input in services
- Consistent ProblemDetails extensions for machine-readable error codes
- Pagination applied in the service/repository, not in memory over full tables
- Versioned routes (`/api/v1/`) when clients depend on stability
- Idempotency for retryable writes where duplicates are costly

## Avoid Entity Leakage

```csharp
// Avoid
[HttpGet("{id:guid}")]
public async Task<OrderEntity> Get(Guid id) =>
    await db.Orders.FindAsync(id) ?? throw new OrderNotFoundException(id);

// Prefer
[HttpGet("{id:guid}")]
public async Task<OrderResponse> Get(Guid id, CancellationToken cancellationToken) =>
    await orderService.GetAsync(id, cancellationToken);
```
