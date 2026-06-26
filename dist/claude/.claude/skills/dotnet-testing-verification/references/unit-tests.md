# Unit Tests

## Naming and Structure

Use descriptive method names: `MethodName_StateUnderTest_ExpectedBehavior`.

```csharp
public sealed class OrderTests
{
    [Theory]
    [InlineData(0)]
    [InlineData(-1)]
    [InlineData(1001)]
    public void Create_throws_when_quantity_out_of_range(int quantity)
    {
        var ex = Assert.Throws<ArgumentOutOfRangeException>(
            () => Order.Create("SKU-1", quantity, DateTimeOffset.UtcNow));

        Assert.Equal("quantity", ex.ParamName);
    }

    [Fact]
    public void ApplyCoupon_reduces_total_once_when_called_twice()
    {
        var order = new Order(new Money(100m, "USD"));

        order.ApplyCoupon("SAVE10");
        order.ApplyCoupon("SAVE10");

        Assert.Equal(90m, order.Total.Amount);
    }
}
```

## Mocking With NSubstitute

```csharp
public sealed class OrderServiceTests
{
    private readonly IOrderRepository _repository = Substitute.For<IOrderRepository>();
    private readonly IClock _clock = Substitute.For<IClock>();
    private readonly OrderService _sut;

    public OrderServiceTests()
    {
        _clock.UtcNow.Returns(new DateTimeOffset(2026, 6, 25, 12, 0, 0, TimeSpan.Zero));
        _sut = new OrderService(_repository, _clock);
    }

    [Fact]
    public async Task GetAsync_throws_when_order_missing()
    {
        _repository.FindByIdAsync(Arg.Any<Guid>(), Arg.Any<CancellationToken>())
            .Returns((Order?)null);

        await Assert.ThrowsAsync<OrderNotFoundException>(
            () => _sut.GetAsync(Guid.NewGuid(), CancellationToken.None));
    }
}
```

Verify interactions only when the collaboration is the contract:

```csharp
await _repository.Received(1).AddAsync(
    Arg.Is<Order>(o => o.Sku == "SKU-1"),
    Arg.Any<CancellationToken>());
```

## Parameterized and Edge Cases

```csharp
[Theory]
[MemberData(nameof(InvalidSkus))]
public async Task CreateAsync_returns_validation_error_for_invalid_sku(string sku)
{
    var result = await _validator.ValidateAsync(new CreateOrderRequest { Sku = sku, Quantity = 1 });
    Assert.False(result.IsValid);
}

public static IEnumerable<object[]> InvalidSkus() =>
    new[] { "", "   ", new string('x', 65) }.Select(s => new object[] { s });
```

## Unit Test Checklist

- One logical assertion focus per test when possible
- No file I/O, network, or database in pure unit tests
- Use `CancellationToken.None` explicitly in sync-style async tests
- Freeze time via `IClock` or `TimeProvider` — do not depend on `DateTime.UtcNow` in assertions
