---
name: angular-state-management
description: Choose and implement state in Angular apps with signals, services, RxJS stores, and NgRx when appropriate. Use when fixing scattered state, stale UI, prop drilling, or deciding between component state, signal stores, and global state libraries.
---

# Angular State Management

## Workflow

1. Classify state: local UI, shared feature state, server/cache data, URL state, auth session.
2. Keep server data in services with Observables or httpResource/signal-based loaders — avoid duplicating API cache in NgRx without cause.
3. Use component signals or local state for ephemeral UI (panel open, step index).
4. Use feature services or signal stores for cross-component state within a feature area.
5. Adopt NgRx (store/effects/component-store) when repo already uses it and benefits justify boilerplate.
6. Sync router query params for bookmarkable filters and pagination.
7. Test state transitions and error paths for shared stores.

## References

- Read `references/state-selection.md` for when to use signals, services, router, and NgRx.
- Read `references/ngrx-and-signal-stores.md` for ComponentStore/signal store patterns and NgRx hygiene.

## Checklist

- Single source of truth per datum.
- Immutability when using NgRx reducers.
- Selectors memoized; avoid mapping huge arrays in templates.
- Effects isolate side effects — not components for HTTP when NgRx is standard.
- Auth/session read-mostly via service or dedicated slice.
- DevTools/debug story acceptable for chosen approach.

## Output

Summarize state categories, pattern chosen, files changed, migration notes, and tests.
