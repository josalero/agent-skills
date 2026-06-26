# Component Patterns

## Presentational vs Container

```tsx
// Presentational — UI only
type OrderSummaryProps = {
  orderId: string;
  status: OrderStatus;
  total: string;
  onViewDetails: (id: string) => void;
};

export function OrderSummary({ orderId, status, total, onViewDetails }: OrderSummaryProps) {
  return (
    <article className="rounded-lg border p-4">
      <h2 className="text-base font-medium">Order {orderId}</h2>
      <p className="text-sm text-muted-foreground">{status}</p>
      <p className="mt-2 font-semibold">{total}</p>
      <button type="button" className="mt-3 text-sm underline" onClick={() => onViewDetails(orderId)}>
        View details
      </button>
    </article>
  );
}
```

```tsx
// Container — data and handlers
export function OrderSummaryContainer({ orderId }: { orderId: string }) {
  const { data, isLoading, error } = useOrder(orderId);
  const navigate = useNavigate();

  if (isLoading) return <OrderSummarySkeleton />;
  if (error) return <ErrorState message="Could not load order" />;
  if (!data) return <EmptyState message="Order not found" />;

  return (
    <OrderSummary
      orderId={data.id}
      status={data.status}
      total={data.totalFormatted}
      onViewDetails={(id) => navigate(`/orders/${id}`)}
    />
  );
}
```

## Composition Over Configuration

Prefer `children` and slots over many boolean flags.

```tsx
// Avoid
<Dialog isAlert isWide showFooter hideClose />

// Prefer
<Dialog>
  <DialogHeader>...</DialogHeader>
  <DialogBody>...</DialogBody>
  <DialogFooter>...</DialogFooter>
</Dialog>
```

## Compound Components (When Justified)

Use when subparts share implicit state and API surface should stay cohesive — document the pattern in the parent file.

## File Colocation

```text
OrderSummary/
  OrderSummary.tsx
  OrderSummary.test.tsx
  index.ts
```

Export public API from `index.ts`; keep helpers private to the folder.
