# Eval: React State Management

## Prompt

Orders list is fetched in three pages, each keeping its own copy in `useState`, causing stale data after cancel on the detail page. Recommend a state approach and implement the smallest fix.

## Expected Agent Behavior

- Identifies duplicated server state as root cause
- Recommends TanStack Query or shared cache with invalidation on mutation
- Avoids global Redux for entire app if query library suffices
- Shows invalidate/refetch or optimistic update pattern
- Mentions tests for cancel flow

## Failure Signals

- Prop drills callback chain only without fixing cache
- Puts all app state in Context
- window.location.reload as fix
