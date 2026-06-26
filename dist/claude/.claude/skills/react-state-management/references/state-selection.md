# State Selection Guide

| State type | Preferred tool | Example |
| --- | --- | --- |
| Toggle, input draft | `useState` in component | modal open, field value |
| Shared between few siblings | Lift to parent | selected tab in wizard step |
| Bookmarkable UI | URL search params | filters, page, sort |
| Remote data | TanStack Query / similar | orders list, user profile |
| Auth session (read-mostly) | Context + hook | current user, roles |
| Cross-route client UI | Zustand / Redux slice | cart, multi-step builder |

## Server State Example (TanStack Query)

```tsx
export function useOrders(status?: OrderStatus) {
  return useQuery({
    queryKey: ["orders", status],
    queryFn: () => api.listOrders({ status }),
    staleTime: 30_000,
  });
}
```

Do not copy `data` into Zustand unless offline or optimistic UX requires it.

## URL State Example

```tsx
const [searchParams, setSearchParams] = useSearchParams();
const page = Number(searchParams.get("page") ?? "0");

const setPage = (next: number) => {
  searchParams.set("page", String(next));
  setSearchParams(searchParams, { replace: true });
};
```

## When Context Is Enough

```tsx
type AuthContextValue = {
  user: User | null;
  signOut: () => void;
};

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
```

Context values should change infrequently — split contexts if needed (theme vs auth).

## Red Flags

- Global store for every fetch result
- Context holding fast-updating mouse position for whole app
- Prop drilling through 6 layers when URL or query fits
- Mutable objects shared without sync strategy
