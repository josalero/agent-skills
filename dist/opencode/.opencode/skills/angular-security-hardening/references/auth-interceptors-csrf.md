# Auth Interceptors and CSRF

## Bearer Interceptor (Token in Memory)

```typescript
export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const auth = inject(AuthService);
  const token = auth.accessToken();
  if (!token) return next(req);
  return next(req.clone({ setHeaders: { Authorization: `Bearer ${token}` } }));
};
```

Register:

```typescript
provideHttpClient(withInterceptors([authInterceptor]));
```

## Cookie Session With CSRF

```typescript
export const csrfInterceptor: HttpInterceptorFn = (req, next) => {
  if (req.method === "GET" || req.method === "HEAD") return next(req);
  const csrf = inject(CsrfService).token();
  return next(req.clone({ setHeaders: { "X-CSRF-Token": csrf } }));
};
```

HttpClient requests must use `withCredentials: true` when cookies authenticate cross-origin according to CORS policy.

## Environment Variables

```typescript
export const environment = {
  production: true,
  apiBaseUrl: "/api/v1",
};
```

`environment.ts` is public in client builds — no OpenAI/private keys here.

## Route Guard (UX Only)

```typescript
export const authGuard: CanActivateFn = () =>
  inject(AuthService).isAuthenticated() || inject(Router).createUrlTree(["/login"]);
```

Pair with API 403 tests — guard alone is not security.

## Logout

```typescript
logout(): Observable<void> {
  return this.http.post<void>("/auth/logout", {}).pipe(
    tap(() => this.session.clear()),
  );
}
```

Clear client caches (NgRx/store) on logout.
