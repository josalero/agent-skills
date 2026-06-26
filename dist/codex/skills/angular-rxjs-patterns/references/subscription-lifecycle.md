# Subscription Lifecycle

## async Pipe in Template (Preferred)

```typescript
@Component({
  template: `
    @if (orders$ | async; as orders) {
      @for (order of orders; track order.id) {
        <app-order-row [order]="order" />
      }
    }
  `,
})
export class OrderListComponent {
  readonly orders$ = this.orderService.list();
}
```

## takeUntilDestroyed in Component Class

```typescript
export class LegacyPanelComponent {
  private readonly destroyRef = inject(DestroyRef);

  constructor(private readonly events: EventBus) {
    this.events.updates$.pipe(takeUntilDestroyed(this.destroyRef)).subscribe((e) => this.apply(e));
  }
}
```

## Avoid Nested Subscribe

```typescript
// Avoid
this.route.paramMap.subscribe((params) => {
  this.orders.get(params.get("id")!).subscribe((order) => (this.order = order));
});

// Prefer
readonly order$ = this.route.paramMap.pipe(
  map((params) => params.get("id")),
  filter((id): id is string => !!id),
  switchMap((id) => this.orders.get(id)),
);
```

## shareReplay Use Carefully

```typescript
private readonly cache$ = this.http.get<User>("/api/v1/me").pipe(
  shareReplay({ bufferSize: 1, refCount: true }),
);
```

Without `refCount`, hot caches may leak after subscribers unsubscribe — document TTL or reset strategy.

## Signals Interop (Angular 16+)

When repo uses signals, prefer `toSignal()` for one-shot HTTP loads with explicit initial value — still handle errors via `catchError` before conversion.
