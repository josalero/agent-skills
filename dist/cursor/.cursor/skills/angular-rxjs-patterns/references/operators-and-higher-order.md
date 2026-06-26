# Operators and Higher-Order Mapping

## Search With switchMap (Cancel Stale Requests)

```typescript
readonly results$ = this.searchControl.valueChanges.pipe(
  debounceTime(250),
  distinctUntilChanged(),
  filter((term): term is string => !!term && term.length >= 2),
  switchMap((term) =>
    this.catalog.search(term).pipe(
      catchError(() => of([])),
    )),
  startWith([]),
);
```

## Form Submit With exhaustMap (Ignore Double-Click)

```typescript
submit$ = new Subject<CreateOrderRequest>();

readonly saveResult$ = this.submit$.pipe(
  exhaustMap((payload) =>
    this.orders.create(payload).pipe(
      map((order) => ({ ok: true as const, order })),
      catchError((err: HttpErrorResponse) => of({ ok: false as const, error: err.message })),
    )),
);
```

## forkJoin for Parallel Reads

```typescript
loadDashboard$(): Observable<DashboardVm> {
  return forkJoin({
    orders: this.orders.listSummary(),
    alerts: this.alerts.listOpen(),
  }).pipe(map(({ orders, alerts }) => ({ orders, alerts })));
}
```

## Operator Selection Guide

| Scenario | Operator |
| --- | --- |
| Autocomplete/search | `switchMap` |
| Save button / POST | `exhaustMap` |
| Queue of writes | `concatMap` |
| Parallel independent GETs | `forkJoin` or `combineLatest` |
| Merge all emissions | `mergeMap` (use with concurrency limit if needed) |
