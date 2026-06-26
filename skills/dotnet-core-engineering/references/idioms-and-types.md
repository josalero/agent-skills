# C# Idioms and Types

## Record for Value Types

```csharp
public sealed record Money(decimal Amount, string Currency)
{
    public Money
    {
        if (Amount < 0) throw new ArgumentOutOfRangeException(nameof(Amount));
        ArgumentException.ThrowIfNullOrWhiteSpace(Currency);
    }
}
```

## Pattern Matching

```csharp
public static string Describe(PaymentResult result) => result switch
{
    PaymentResult.Accepted accepted => $"Accepted {accepted.AuthorizationId}",
    PaymentResult.Declined declined => $"Declined {declined.ReasonCode}",
    PaymentResult.Pending pending => $"Pending {pending.Reference}",
    _ => throw new ArgumentOutOfRangeException(nameof(result))
};
```

## Nullable Reference Types

```csharp
public Order? FindById(Guid id) =>
    _store.TryGetValue(id, out var order) ? order : null;

public Order GetRequired(Guid id) =>
    FindById(id) ?? throw new OrderNotFoundException(id);
```

Enable `<Nullable>enable</Nullable>` project-wide; avoid `!` suppression without comment.
