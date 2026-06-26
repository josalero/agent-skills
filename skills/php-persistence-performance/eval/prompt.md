# Eval: PHP Persistence Performance

## Prompt

This order list endpoint is slow under load. Diagnose the persistence issue and fix it with the smallest safe change. Add or update a test that would catch an N+1 regression.

```php
<?php

class OrderController
{
    public function index(Request $request, OrderRepository $orders): JsonResponse
    {
        $customerId = $request->integer('customerId');

        $payload = array_map(
            static fn (Order $order): array => [
                'id' => $order->id,
                'status' => $order->status,
                'lineCount' => count($order->lines),
                'skus' => array_map(static fn ($line) => $line->sku, $order->lines),
            ],
            $orders->findByCustomerId($customerId),
        );

        return response()->json($payload);
    }
}
```

## Expected Agent Behavior

- Identifies lazy-loading N+1 when accessing `$order->lines` per order
- Proposes eager load, join fetch, or projection instead of loading full graphs blindly
- Keeps pagination or warns if the endpoint returns unbounded lists
- Adds an integration test or documents query-count verification approach
- Summarizes root cause, fix, and verification command

## Failure Signals

- Adds global eager loading on all associations without scope
- Wraps controller in a transaction without addressing fetch strategy
- Suggests cache as the first fix without measuring query behavior
- Loads all orders into memory before filtering or paginating
