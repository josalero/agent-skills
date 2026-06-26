---
name: angular-performance
description: Diagnose and improve Angular change detection, bundle size, lazy loading, and runtime performance. Use when fixing slow UI, unnecessary re-renders, large initial bundles, or list rendering performance in Angular apps.
---

# Angular Performance

## Workflow

1. Measure with Angular DevTools, Chrome Performance, and source-map explorer — establish baseline.
2. Identify issue class: change detection churn, bundle size, hydration (if SSR), heavy templates, or unvirtualized lists.
3. Apply OnPush change detection where inputs/streams are stable.
4. Lazy-load routes and defer non-critical imports; audit third-party library weight.
5. Use trackBy/`@for` track expressions; virtualize large lists when needed.
6. Avoid expensive work in template functions — move to pipes with pure strategy or precomputed view models.
7. Re-measure after each change; document tradeoffs.

## References

- Read `references/change-detection-and-templates.md` for OnPush, signals, and template cost.
- Read `references/bundle-and-lazy-loading.md` for route lazy loading and bundle analysis.

## Checklist

- Default change detection justified where OnPush not used.
- No heavy computation in template interpolation without memoization.
- Routes for large features are lazy loaded.
- Images/assets optimized; unused polyfills removed.
- SSR/hydration mismatches investigated if using Angular Universal.
- List views track items by stable id.

## Output

Summarize baseline, root cause, optimizations applied, after metrics, and verification steps.
