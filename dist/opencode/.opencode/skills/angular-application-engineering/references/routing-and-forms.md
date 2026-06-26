# Routing and Forms

## Lazy Standalone Route

```typescript
export const routes: Routes = [
  {
    path: "orders",
    loadComponent: () => import("./orders/order-list.component").then((m) => m.OrderListComponent),
    canActivate: [authGuard],
  },
  {
    path: "orders/:id",
    loadComponent: () => import("./orders/order-page.component").then((m) => m.OrderPageComponent),
    canActivate: [authGuard],
  },
];
```

## Functional Auth Guard

```typescript
export const authGuard: CanActivateFn = () => {
  const auth = inject(AuthService);
  const router = inject(Router);
  if (auth.isAuthenticated()) {
    return true;
  }
  return router.createUrlTree(["/login"]);
};
```

## Typed Reactive Form

```typescript
type CreateOrderForm = {
  sku: FormControl<string>;
  quantity: FormControl<number>;
};

@Component({
  standalone: true,
  imports: [ReactiveFormsModule],
  template: `
    <form [formGroup]="form" (ngSubmit)="submit()">
      <input formControlName="sku" aria-label="SKU" />
      @if (form.controls.sku.invalid && form.controls.sku.touched) {
        <p role="alert">SKU is required</p>
      }
      <input type="number" formControlName="quantity" aria-label="Quantity" />
      <button type="submit" [disabled]="form.invalid">Place order</button>
    </form>
  `,
})
export class CreateOrderComponent {
  readonly form = new FormGroup<CreateOrderForm>({
    sku: new FormControl("", { nonNullable: true, validators: [Validators.required] }),
    quantity: new FormControl(1, {
      nonNullable: true,
      validators: [Validators.required, Validators.min(1), Validators.max(1000)],
    }),
  });

  private readonly orders = inject(OrderService);

  submit(): void {
    if (this.form.invalid) return;
    this.orders.create(this.form.getRawValue()).subscribe();
  }
}
```

## NgModule Apps (Legacy)

If the repo uses NgModules, match existing `declarations` / `imports` structure — do not mass-convert to standalone in unrelated PRs.
