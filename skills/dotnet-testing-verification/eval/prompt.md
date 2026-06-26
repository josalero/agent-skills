# Eval: .NET Testing Verification

## Prompt

Bug report: applying the same coupon twice reduces the order total twice. Fix the bug and add tests that would have caught it. The project uses xUnit and NSubstitute.

```csharp
public sealed class Order
{
    private decimal _total;
    private bool _couponApplied;

    public Order(decimal total) => _total = total;

    public void ApplyCoupon(string code)
    {
        if (code == "SAVE10")
        {
            _total *= 0.90m;
            _couponApplied = true;
        }
    }

    public decimal Total => _total;
}
```

## Expected Agent Behavior

- Adds regression test reproducing double-discount failure
- Fixes logic with idempotency guard or explicit state check
- Uses behavior-focused assertions on `Total`, not private fields
- Runs targeted `dotnet test --filter` command first
- Summarizes test type chosen and verification command

## Failure Signals

- Fixes code without regression test
- Tests private fields via reflection
- Runs entire solution without mentioning narrower command first
- Adds WebApplicationFactory for pure unit logic
