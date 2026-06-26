# Async and Errors

## Async All the Way

```csharp
public async Task<OrderResponse> CreateAsync(CreateOrderRequest request, CancellationToken cancellationToken)
{
    var order = Order.Create(request);
    await _repository.AddAsync(order, cancellationToken);
    return OrderMapper.ToResponse(order);
}
```

Avoid `.Result` and `.Wait()` on async paths — causes deadlocks and thread-pool starvation.

## CancellationToken Propagation

Pass `CancellationToken` from ASP.NET request through services to EF/HTTP calls.

## Domain Exceptions vs Problem Details

Throw domain exceptions (`OrderNotFoundException`) in core logic; map to HTTP in API layer — not in domain services for web-specific types.

## IAsyncEnumerable for Streaming

```csharp
public async IAsyncEnumerable<OrderSummary> StreamSummariesAsync(
    [EnumeratorCancellation] CancellationToken cancellationToken = default)
{
    await foreach (var order in _repository.StreamAllAsync(cancellationToken))
    {
        yield return OrderMapper.ToSummary(order);
    }
}
```
