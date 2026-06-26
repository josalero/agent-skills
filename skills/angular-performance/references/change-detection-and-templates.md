# Change Detection and Templates

## OnPush Component

```typescript
@Component({
  selector: "app-order-row",
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `<tr><td>{{ order.id }}</td><td>{{ order.status }}</td></tr>`,
})
export class OrderRowComponent {
  @Input({ required: true }) order!: OrderSummary;
}
```

Ensure parent passes new object references only when data changes, or use async pipe/signals for updates.

## @for With Track

```typescript
@for (order of orders; track order.id) {
  <app-order-row [order]="order" />
}
```

## Avoid Template Method Calls

```typescript
// Avoid — runs every change detection cycle
{{ formatTotal(order) }}

// Prefer — map in component or pure pipe
{{ order.totalFormatted }}
```

## Signals for Local View State (Modern Angular)

```typescript
readonly query = signal("");
readonly filtered = computed(() =>
  this.orders().filter((o) => o.id.includes(this.query())),
);
```

Use when repo already adopts signals — do not mix paradigms inconsistently within one feature.

## DevTools Checklist

- Profile component tree time during typing/filtering
- Look for components with high change detection count
- Verify async pipe unsubscribes automatically
