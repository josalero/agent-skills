---
name: react-state-management
description: Choose and implement React state patterns including local state, lifted state, context, URL state, and external stores. Use when fixing prop drilling, inconsistent shared state, stale closures, or deciding between Context, Zustand, Redux, or server-state libraries like TanStack Query.
---

# React State Management

## Workflow

1. Classify state: UI ephemeral, form draft, shared client state, server/cache state, or URL-addressable state.
2. Prefer the simplest owner: `useState` locally until a second consumer needs the data.
3. Use URL/search params for shareable filters, tabs, and pagination when appropriate.
4. Use server-state tools (TanStack Query, SWR, RTK Query) for remote data — do not duplicate server data in global client stores without reason.
5. Reach for Context for low-churn theming/auth locale — not high-frequency updates across large trees.
6. Use focused external stores (Zustand/Redux) when many distant components need coordinated writes with clear actions.
7. Verify with tests simulating user flows and concurrent updates.

## References

- Read `references/state-selection.md` for when to use local, URL, server, context, and store state.
- Read `references/context-and-stores.md` for Context patterns, Zustand slices, and anti-patterns.

## Checklist

- Single source of truth per datum — no duplicated server cache.
- State updates are immutable and predictable.
- Derived values use `useMemo` only when measurement shows need.
- Async race conditions handled (abort, request id, or query library dedupe).
- Form state colocated with form unless truly shared.
- DevTools/debug story acceptable for chosen store.

## Output

Summarize state types identified, pattern chosen, files changed, migration notes, and tests covering shared-state behavior.
