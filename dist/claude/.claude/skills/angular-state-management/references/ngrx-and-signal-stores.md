# NgRx and Signal Stores

## ComponentStore (Feature-Local)

```typescript
@Injectable()
export class OrderFiltersStore extends ComponentStore<OrderFiltersState> {
  constructor() {
    super({ status: "OPEN", query: "" });
  }

  readonly vm$ = this.select(({ status, query }) => ({ status, query }));

  readonly setStatus = this.updater((state, status: OrderStatus) => ({ ...state, status }));
  readonly setQuery = this.updater((state, query: string) => ({ ...state, query }));
}
```

Provide at feature/route level — not root unless truly global.

## NgRx Effect for Side Effect

```typescript
loadOrders$ = createEffect(() =>
  this.actions$.pipe(
    ofType(OrdersActions.load),
    switchMap(({ filters }) =>
      this.api.list(filters).pipe(
        map((orders) => OrdersActions.loadSuccess({ orders })),
        catchError((error) => of(OrdersActions.loadFailure({ error }))),
      )),
  ),
);
```

Keep effects thin — map API DTOs in services if needed.

## Selectors

```typescript
export const selectOpenOrders = createSelector(selectAllOrders, (orders) =>
  orders.filter((o) => o.status === "OPEN"),
);
```

Memoization matters for large collections.

## When Not to Add NgRx

If the app has no NgRx and the task is one shared list cache — prefer `OrderService` with `shareReplay` or signals + `httpResource` before introducing global store infrastructure.

## Testing Stores

- ComponentStore: test updaters and selectors directly
- NgRx: use `provideMockStore` or integration tests with reducers/effects
