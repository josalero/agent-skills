# Context and External Stores

## Zustand Slice (Focused Client State)

```tsx
type CartState = {
  items: CartItem[];
  addItem: (item: CartItem) => void;
  removeItem: (sku: string) => void;
  clear: () => void;
};

export const useCartStore = create<CartState>((set) => ({
  items: [],
  addItem: (item) =>
    set((state) => ({
      items: state.items.some((i) => i.sku === item.sku)
        ? state.items.map((i) => (i.sku === item.sku ? { ...i, qty: i.qty + item.qty } : i))
        : [...state.items, item],
    })),
  removeItem: (sku) => set((state) => ({ items: state.items.filter((i) => i.sku !== sku) })),
  clear: () => set({ items: [] }),
}));
```

Keep actions colocated; selectors prevent unnecessary re-renders:

```tsx
const itemCount = useCartStore((s) => s.items.reduce((n, i) => n + i.qty, 0));
```

## Redux Toolkit (When Already in Repo)

Match existing slice patterns — do not introduce Redux for a single toggle.

## Optimistic Updates

Prefer query library optimistic helpers; if manual:

```tsx
const mutation = useMutation({
  mutationFn: api.updateOrder,
  onMutate: async (payload) => {
    await queryClient.cancelQueries({ queryKey: ["orders"] });
    const previous = queryClient.getQueryData<Order[]>(["orders"]);
    queryClient.setQueryData(["orders"], (old: Order[] = []) =>
      old.map((o) => (o.id === payload.id ? { ...o, ...payload } : o)));
    return { previous };
  },
  onError: (_err, _payload, context) => {
    queryClient.setQueryData(["orders"], context?.previous);
  },
});
```

## Testing Shared State

- Reset store between tests (`useCartStore.setState({ items: [] })`)
- Render with providers under test (`QueryClientProvider`, `AuthProvider`)
- Assert user-visible outcomes, not internal store shape alone
