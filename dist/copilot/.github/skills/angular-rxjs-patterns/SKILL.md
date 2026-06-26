---
name: angular-rxjs-patterns
description: Apply RxJS patterns correctly in Angular apps including async pipe, higher-order mapping, error handling, and subscription lifecycle. Use when fixing memory leaks, race conditions, duplicate HTTP calls, or refactoring Observable-based services and components.
---

# Angular RxJS Patterns

## Workflow

1. Identify stream sources: HTTP, forms, router events, websockets, store selectors.
2. Prefer `async` pipe or `takeUntilDestroyed()` over manual subscribe in components.
3. Choose operators deliberately: `switchMap` for search, `exhaustMap` for submits, `concatMap` for ordered writes.
4. Handle errors inside streams — do not break the whole chain silently.
5. Avoid nested subscribes; flatten with higher-order operators.
6. Share hot observables with `shareReplay` only when needed and bounded.
7. Verify with marble-style reasoning or tests using `TestScheduler` when logic is complex.

## References

- Read `references/operators-and-higher-order.md` for switchMap/exhaustMap/catchError patterns.
- Read `references/subscription-lifecycle.md` for async pipe, takeUntilDestroyed, and shareReplay.

## Checklist

- No nested `subscribe` in components without strong justification.
- HTTP calls deduplicated or cancelled appropriately for use case.
- Loading/error states derived from stream, not duplicated flags.
- Subscriptions tied to component/directive lifecycle.
- `debounceTime`/`distinctUntilChanged` on user input search streams.
- Tests cover error and retry behavior where critical.

## Output

Summarize stream graph changes, operator choices, lifecycle fixes, and tests/commands run.
