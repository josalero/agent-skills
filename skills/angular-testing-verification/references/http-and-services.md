# HTTP and Service Tests

## HttpClientTestingModule

```typescript
describe("OrderService", () => {
  let service: OrderService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [OrderService],
    });
    service = TestBed.inject(OrderService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => httpMock.verify());

  it("loads order by id", () => {
    let result: OrderSummary | undefined;
    service.getOrder("ORD-1").subscribe((state) => {
      if (state.order) result = state.order;
    });

    const req = httpMock.expectOne("/api/v1/orders/ORD-1");
    expect(req.request.method).toBe("GET");
    req.flush({ id: "ORD-1", status: "OPEN", totalFormatted: "$10" });

    expect(result?.id).toBe("ORD-1");
  });
});
```

## Error Path

```typescript
it("maps HTTP error to state", () => {
  let error: string | null = null;
  service.getOrder("missing").subscribe((state) => (error = state.error));

  const req = httpMock.expectOne("/api/v1/orders/missing");
  req.flush("Not found", { status: 404, statusText: "Not Found" });

  expect(error).toBeTruthy();
});
```

## Spy When Testing Pure Logic Service

Use Jasmine spies or Jest mocks for collaborators — not for HttpClient when integration-style test is intended.

## CI Commands

```bash
ng test --watch=false --browsers=ChromeHeadless
npm test -- --runInBand
```

Use the script defined in the project's `package.json` / `angular.json`.
