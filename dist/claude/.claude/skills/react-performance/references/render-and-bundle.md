# Render and Bundle Optimization

## React Profiler Workflow

1. Record interaction (filter change, tab switch)
2. Note components with high render count or duration
3. Inspect props changing each render (inline functions/objects)

## Route Code Splitting (Vite/React Router)

```tsx
const AdminReports = lazy(() => import("./pages/AdminReports"));

export function AppRoutes() {
  return (
    <Suspense fallback={<PageSkeleton />}>
      <Routes>
        <Route path="/admin/reports" element={<AdminReports />} />
      </Routes>
    </Suspense>
  );
}
```

## Bundle Analysis

```bash
npm run build
npx vite-bundle-visualizer
# or project-specific analyze script
```

Look for duplicate lodash/moment versions and heavy chart/editor libraries on critical path.

## `useMemo` / `useCallback` When Justified

```tsx
const sortedOrders = useMemo(
  () => [...orders].sort((a, b) => a.createdAt.localeCompare(b.createdAt)),
  [orders],
);

const handleSelect = useCallback((id: string) => setSelectedId(id), []);
```

Skip if sort is cheap and list is small — measure first.

## Context Splitting

Split theme vs session vs high-frequency data to reduce subtree re-renders.

## SSR / Hydration Notes

Hydration mismatches cause expensive client rework — ensure server and client render same initial HTML; defer browser-only APIs to `useEffect`.
