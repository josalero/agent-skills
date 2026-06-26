# Breaking Changes Checklist

## Control Flow Syntax (v17+)

```typescript
// Before
<div *ngIf="user">{{ user.name }}</div>
<div *ngFor="let item of items">{{ item }}</div>

// After
@if (user) {
  <div>{{ user.name }}</div>
}
@for (item of items; track item.id) {
  <div>{{ item.name }}</div>
}
```

Run official schematic where available — do not mix inconsistently in one template without reason.

## Standalone Components

```typescript
@Component({
  standalone: true,
  imports: [CommonModule, RouterLink],
  // ...
})
```

Update TestBed imports to match standalone `imports` array.

## Functional Guards and Interceptors

```typescript
export const authGuard: CanActivateFn = () => inject(AuthService).isAuthenticated() || inject(Router).createUrlTree(["/login"]);
```

Replace class-based guards incrementally.

## RxJS 7+

Most Angular apps already on RxJS 7. Verify import paths and remove legacy patch operators if migrating very old code.

## Deprecated API Scan

```bash
ng build 2>&1 | rg -i deprecat
```

Track deprecations as tickets — do not ignore warnings indefinitely.

## Verify

```bash
ng serve
ng test --watch=false
ng build --configuration=production
```

Smoke login and one critical workflow manually after production build.
