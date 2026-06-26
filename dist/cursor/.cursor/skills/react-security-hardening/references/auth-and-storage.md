# Auth and Client Storage

## Public Env Vars (Vite)

```ts
// Exposed to browser — public only
const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;
```

Never put private API keys in `VITE_*` variables.

## Prefer HttpOnly Session Cookies

When backend controls auth:

- Session token in HttpOnly, Secure, SameSite cookie
- Frontend uses `fetch(..., { credentials: "include" })`
- CSRF token header or double-submit cookie for mutating requests

```tsx
await fetch("/api/v1/orders", {
  method: "POST",
  credentials: "include",
  headers: {
    "Content-Type": "application/json",
    "X-CSRF-Token": csrfToken,
  },
  body: JSON.stringify(payload),
});
```

## Bearer Token in Memory (SPA Alternative)

If using JWT in memory:

- Avoid localStorage when XSS is in threat model
- Short-lived access token + refresh flow with rotation
- Clear on logout/tab close strategy documented

## Client Route Guards

```tsx
if (!user) return <Navigate to="/login" replace />;
```

Always enforce authorization on API — client guard is UX only.

## Dependency Audit

```bash
npm audit --production
npm run build
```

Fix or document exceptions for critical findings before release.

## Logout

```tsx
async function logout() {
  await api.post("/auth/logout");
  queryClient.clear();
  authStore.reset();
}
```

Ensure server invalidates session; client-only logout is insufficient.
