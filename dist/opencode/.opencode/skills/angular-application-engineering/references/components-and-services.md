# Components and Services

## Standalone Presentational Component

```typescript
@Component({
  selector: "app-order-summary",
  standalone: true,
  imports: [CommonModule],
  template: `
    <article class="order-summary">
      <h2>Order {{ order.id }}</h2>
      <p>{{ order.status }}</p>
      <p class="total">{{ order.totalFormatted }}</p>
      <button type="button" (click)="viewDetails.emit(order.id)">View details</button>
    </article>
  `,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class OrderSummaryComponent {
  @Input({ required: true }) order!: OrderSummary;
  @Output() viewDetails = new EventEmitter<string>();
}
```

## Smart Container With Service

```typescript
@Component({
  selector: "app-order-page",
  standalone: true,
  imports: [OrderSummaryComponent, LoadingStateComponent, ErrorStateComponent],
  template: `
    @if (state$ | async; as state) {
      @if (state.loading) { <app-loading-state /> }
      @else if (state.error) { <app-error-state [message]="state.error" /> }
      @else if (state.order) {
        <app-order-summary [order]="state.order" (viewDetails)="onView($event)" />
      }
    }
  `,
})
export class OrderPageComponent {
  private readonly orders = inject(OrderService);
  private readonly router = inject(Router);
  readonly state$ = this.orders.getOrder(this.route.snapshot.paramMap.get("id")!);

  constructor(private readonly route: ActivatedRoute) {}

  onView(id: string): void {
    void this.router.navigate(["/orders", id, "details"]);
  }
}
```

## Service With HttpClient

```typescript
@Injectable({ providedIn: "root" })
export class OrderService {
  private readonly http = inject(HttpClient);

  getOrder(id: string): Observable<OrderState> {
    return this.http.get<OrderSummary>(`/api/v1/orders/${id}`).pipe(
      map((order) => ({ loading: false, error: null, order })),
      startWith({ loading: true, error: null, order: null }),
      catchError((err: HttpErrorResponse) =>
        of({ loading: false, error: err.message, order: null })),
    );
  }
}
```

Match existing project patterns for signals vs observables — do not mix without reason.
