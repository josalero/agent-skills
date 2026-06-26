# Eval: React Performance

## Prompt

Filtering a 5,000-row table in React causes 2s UI freeze on each keystroke. Diagnose and fix with minimal scope.

## Expected Agent Behavior

- Profiles render cost; identifies full-table re-render/filter on main thread
- Recommends debounce, memoized rows, virtualization, or server-side filter
- Measures before/after approach
- Avoids memo everywhere without diagnosis

## Failure Signals

- Suggests `useMemo` on container only with no list strategy
- Moves filter to backend without discussing API
- Ignores measurement
