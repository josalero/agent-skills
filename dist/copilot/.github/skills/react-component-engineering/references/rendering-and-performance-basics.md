# Rendering and Performance Basics

## Stable List Keys

```tsx
{orders.map((order) => (
  <OrderRow key={order.id} order={order} />
))}
```

Do not use index as key when list order changes or items are edited/deleted.

## Conditional Rendering

```tsx
if (isLoading) return <Spinner aria-label="Loading orders" />;
if (error) return <ErrorBanner message={error.message} />;
if (orders.length === 0) return <EmptyState title="No orders yet" />;

return <OrderTable orders={orders} />;
```

Avoid nested ternaries spanning multiple lines — extract subcomponents.

## When to Use `memo`

```tsx
export const OrderRow = memo(function OrderRow({ order, onSelect }: OrderRowProps) {
  return (/* ... */);
});
```

Use when:

- Row re-renders often in large lists
- Props are stable or cheap to compare

Skip when:

- Component is already cheap
- Props change every parent render anyway

Profile before memoizing everything.

## Avoid Inline Object/Function Props in Hot Lists

```tsx
// Causes child memo to bail out every render
<OrderRow order={order} onSelect={() => select(order.id)} />

// Better — stable handler from parent or row id callback
const handleSelect = useCallback((id: string) => select(id), [select]);
```

## Semantic Elements

Use `button`, `a`, `label`, `nav`, `main` — not clickable `div`s without roles and keyboard support.
