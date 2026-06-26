# TestBed and Components

## Standalone Component Test

```typescript
describe("OrderSummaryComponent", () => {
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [OrderSummaryComponent],
    }).compileComponents();
  });

  it("emits viewDetails when button clicked", () => {
    const fixture = TestBed.createComponent(OrderSummaryComponent);
    fixture.componentRef.setInput("order", { id: "ORD-1", status: "OPEN", totalFormatted: "$10" });
    fixture.detectChanges();

    const spy = jasmine.createSpy("viewDetails");
    fixture.componentInstance.viewDetails.subscribe(spy);

    const button = fixture.nativeElement.querySelector("button");
    button.click();

    expect(spy).toHaveBeenCalledWith("ORD-1");
  });
});
```

## Query by Role / Label (Preferred)

Use `@testing-library/angular` when project already includes it:

```typescript
const { getByRole } = await render(CreateOrderComponent);
await userEvent.click(getByRole("button", { name: /place order/i }));
```

## detectChanges vs whenStable

```typescript
fixture.detectChanges();
await fixture.whenStable();
```

Use `whenStable` after async pipe resolves microtasks or fakeAsync tests complete.

## Router Outlet Test Stub

```typescript
await TestBed.configureTestingModule({
  imports: [OrderPageComponent, RouterTestingModule.withRoutes([])],
}).compileComponents();
```
