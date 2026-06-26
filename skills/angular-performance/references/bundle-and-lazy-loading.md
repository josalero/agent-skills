# Bundle and Lazy Loading

## Lazy Feature Route

```typescript
{
  path: "admin",
  loadChildren: () => import("./admin/admin.routes").then((m) => m.ADMIN_ROUTES),
}
```

For standalone:

```typescript
loadComponent: () => import("./reports/reports.component").then((m) => m.ReportsComponent),
```

## Defer Block (Angular 17+)

```typescript
@defer (on viewport) {
  <app-heavy-chart [data]="chartData" />
} @placeholder {
  <p>Loading chart…</p>
}
```

Use for below-the-fold or non-critical widgets.

## Bundle Analysis

```bash
ng build --configuration=production --stats-json
npx webpack-bundle-analyzer dist/your-app/stats.json
```

Identify duplicate RxJS/operators and moment/lodash imports — prefer tree-shakable paths.

## Prefetch Strategy

Configure router preloading only when measured benefit exists:

```typescript
provideRouter(routes, withPreloading(PreloadAllModules))
```

Preloading everything can hurt mobile first paint — measure.

## Server-Side Rendering Notes

Hydration errors cause client rework — ensure server and browser render the same initial HTML; defer browser-only APIs to `afterNextRender` / `ngAfterViewInit`.
