# Upgrade Sequencing

## Incremental Major Upgrades

```bash
ng update @angular/core@18 @angular/cli@18
npm test
ng build

ng update @angular/core@19 @angular/cli@19
npm test
ng build
```

Do not skip majors without reading combined breaking change notes — schematics assume sequential path.

## Align Ecosystem Packages

```bash
ng update @angular/material
ng update @ngrx/store   # if used
```

Check UI library release notes for Angular compatibility matrix.

## Standalone Bootstrap Migration

```typescript
// main.ts (modern)
bootstrapApplication(AppComponent, {
  providers: [provideRouter(routes), provideHttpClient(withInterceptors([authInterceptor]))],
});
```

Replace `NgModule` bootstrap only when migration plan includes module removal or new apps.

## TypeScript / Node

- Match Angular version support table for TypeScript
- Use Node LTS in CI (.nvmrc / `.node-version`)

## PR Slicing

| PR | Content |
| --- | --- |
| 1 | Toolchain + Angular bump + compile fixes |
| 2 | Optional standalone/route migrations |
| 3 | Remove deprecated APIs and dead NgModules |

Each PR keeps main deployable when possible.
