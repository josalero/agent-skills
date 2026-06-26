# State Selection in Angular

| State | Tool | Example |
| --- | --- | --- |
| Toggle, field draft | `signal()` / local state | dialog open |
| Shared in feature | Injectable service + signals/BehaviorSubject | wizard step |
| Server lists | Service + Observable or `httpResource` | orders list |
| Bookmarkable filters | Router query params | `?status=OPEN&page=2` |
| Global UI session | AuthService + signals | current user |
| Complex cross-feature | NgRx Store / ComponentStore | existing app standard |

## Signal Service Example

```typescript
@Injectable({ providedIn: "root" })
export class CartStore {
  private readonly items = signal<CartItem[]>([]);
  readonly itemCount = computed(() => this.items().reduce((n, i) => n + i.qty, 0));
  readonly view = computed(() => ({ items: this.items(), itemCount: this.itemCount() }));

  addItem(item: CartItem): void {
    this.items.update((current) => mergeCartItem(current, item));
  }
}
```

## Router Query State

```typescript
readonly filters$ = this.route.queryParamMap.pipe(
  map((params) => ({
    status: params.get("status") ?? "OPEN",
    page: Number(params.get("page") ?? "0"),
  })),
);
```

## Avoid

- NgRx for entire app when most state is server-backed HTTP
- BehaviorSubject everywhere when signals suffice locally
- Mutable arrays stored in NgRx without immutability

Match the dominant pattern already in the repository.
