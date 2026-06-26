# Integration Tests

## WebApplicationFactory Setup

```csharp
public sealed class OrdersApiFactory : WebApplicationFactory<Program>
{
    protected override void ConfigureWebHost(IWebHostBuilder builder)
    {
        builder.UseEnvironment("Testing");
        builder.ConfigureServices(services =>
        {
            var descriptor = services.SingleOrDefault(
                d => d.ServiceType == typeof(DbContextOptions<AppDbContext>));
            if (descriptor is not null)
                services.Remove(descriptor);

            services.AddDbContext<AppDbContext>(options =>
                options.UseInMemoryDatabase("OrdersApiTests"));
        });
    }
}

public sealed class CreateOrderTests(OrdersApiFactory factory) : IClassFixture<OrdersApiFactory>
{
    private readonly HttpClient _client = factory.CreateClient();

    [Fact]
    public async Task Post_returns_201_with_order_id()
    {
        var response = await _client.PostAsJsonAsync("/api/v1/orders", new
        {
            sku = "SKU-1",
            quantity = 2
        });

        Assert.Equal(HttpStatusCode.Created, response.StatusCode);
        var body = await response.Content.ReadFromJsonAsync<OrderResponse>();
        Assert.NotEqual(Guid.Empty, body!.Id);
    }

    [Fact]
    public async Task Post_returns_400_when_quantity_invalid()
    {
        var response = await _client.PostAsJsonAsync("/api/v1/orders", new
        {
            sku = "SKU-1",
            quantity = 0
        });

        Assert.Equal(HttpStatusCode.BadRequest, response.StatusCode);
        var problem = await response.Content.ReadFromJsonAsync<ValidationProblemDetails>();
        Assert.NotNull(problem?.Errors);
    }
}
```

Expose `Program` for test host:

```csharp
// At end of Program.cs
public partial class Program { }
```

## Database Integration With Testcontainers

Use when InMemory provider hides SQL, constraints, or migrations:

```csharp
public sealed class PostgresFixture : IAsyncLifetime
{
    private readonly PostgreSqlContainer _container = new PostgreSqlBuilder()
        .WithImage("postgres:16-alpine")
        .Build();

    public string ConnectionString => _container.GetConnectionString();

    public async Task InitializeAsync() => await _container.StartAsync();
    public async Task DisposeAsync() => await _container.DisposeAsync();
}
```

Apply migrations in fixture setup; run tests against real PostgreSQL behavior.

## Test Type Selection

| Scenario | Prefer |
| --- | --- |
| Business rules, calculations | Unit test |
| Service + repository with in-memory DB | Integration test in service test project |
| HTTP status, binding, ProblemDetails | WebApplicationFactory |
| SQL dialect, indexes, migrations | Testcontainers + EF migrations |

## CI Commands

```bash
# Narrow
dotnet test tests/Orders.UnitTests --filter "FullyQualifiedName~OrderServiceTests"

# Project
dotnet test tests/Orders.IntegrationTests

# Solution with coverage (when configured)
dotnet test --collect:"XPlat Code Coverage"
```

Run the narrowest filter that proves the change before the full suite.

## Integration Test Checklist

- `Testing` environment disables external side effects (email, queues, real payment APIs)
- Seed data is isolated per test or uses transactions/respawn
- Assert on HTTP status, headers, and body shape — not just `IsSuccessStatusCode`
- Clean up IDisposable resources in `IAsyncDisposable` fixtures
