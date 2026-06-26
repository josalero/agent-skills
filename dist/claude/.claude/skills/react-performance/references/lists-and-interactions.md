# Lists and Interaction Latency

## Virtualize Long Lists

```tsx
import { useVirtualizer } from "@tanstack/react-virtual";

export function OrderVirtualList({ orders }: { orders: Order[] }) {
  const parentRef = useRef<HTMLDivElement>(null);
  const virtualizer = useVirtualizer({
    count: orders.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 56,
  });

  return (
    <div ref={parentRef} className="h-96 overflow-auto">
      <div style={{ height: virtualizer.getTotalSize(), position: "relative" }}>
        {virtualizer.getVirtualItems().map((item) => (
          <div
            key={orders[item.index].id}
            style={{
              position: "absolute",
              top: 0,
              transform: `translateY(${item.start}px)`,
              height: item.size,
            }}
          >
            <OrderRow order={orders[item.index]} />
          </div>
        ))}
      </div>
    </div>
  );
}
```

Prefer pagination or infinite query if virtualization adds complexity without need.

## Debounce Expensive Filters

```tsx
const [query, setQuery] = useState("");
const debouncedQuery = useDebouncedValue(query, 250);

useEffect(() => {
  refetch({ query: debouncedQuery });
}, [debouncedQuery, refetch]);
```

## Avoid Layout Thrash

- Batch DOM reads/writes
- Do not measure layout in render — use `useLayoutEffect` sparingly for known UI sync needs

## Interaction Targets

- Input feedback < 100ms perceived
- Route transitions show immediate skeleton, not blank page
- Avoid blocking main thread with sync JSON parse of huge payloads — paginate API
