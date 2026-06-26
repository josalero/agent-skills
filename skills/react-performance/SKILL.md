---
name: react-performance
description: Diagnose and improve React application performance including render cost, memoization, list virtualization, code splitting, and bundle size. Use when fixing slow interactions, unnecessary re-renders, large bundles, or hydration and runtime performance regressions.
---

# React Performance

## Workflow

1. Measure first: React Profiler, browser Performance tab, Lighthouse, or bundle analyzer — do not optimize blindly.
2. Identify bottleneck type: render churn, large lists, expensive effects, network waterfall, or bundle parse cost.
3. Fix highest-impact issues: unstable keys, context churn, unmemoized heavy lists, missing code split on routes.
4. Apply targeted `memo`, `useMemo`, `useCallback` only where profiling shows benefit.
5. Lazy-load routes and heavy components; prefetch critical paths when appropriate.
6. Re-measure after each change; avoid premature micro-optimizations.
7. Document tradeoffs when readability regresses for measurable gain.

## References

- Read `references/render-and-bundle.md` for Profiler usage, splitting, and lazy routes.
- Read `references/lists-and-interactions.md` for virtualization, debouncing, and interaction latency.

## Checklist

- Profiler confirms which components re-render excessively.
- Large lists virtualized or paginated.
- Route-level code splitting for infrequent views.
- Images and fonts optimized; third-party scripts deferred.
- Server components / SSR strategy understood if using Next.js or similar.
- No blanket `memo` on every leaf component.

## Output

Summarize baseline metric, root cause, changes made, after metric, and verification steps.
