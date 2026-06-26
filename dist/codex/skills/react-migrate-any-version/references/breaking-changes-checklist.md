# Breaking Changes Checklist

## React 18+ Root API

```tsx
// Before
ReactDOM.render(<App />, document.getElementById("root"));

// After
createRoot(document.getElementById("root")!).render(<App />);
```

## Strict Mode (Development)

Effects may mount/unmount twice — ensure cleanup functions are correct and idempotent.

## React 19 Notes (Verify Against Project)

- `ref` as prop on function components (when supported by version)
- Stricter hydration warnings — fix server/client HTML mismatches
- Review deprecated APIs removed in target version (e.g. legacy context, string refs)

Always confirm against installed version docs — do not assume blog posts match.

## React Router v5 → v6

```tsx
// v6
<Routes>
  <Route path="/orders" element={<OrdersPage />} />
  <Route path="/orders/:id" element={<OrderDetailPage />} />
</Routes>
```

- `useHistory` → `useNavigate`
- `Switch` → `Routes`
- Relative routes and loaders/actions if adopting data APIs

## Testing Library / act

Prefer `userEvent` + `findBy*` over wrapping everything in manual `act`.

Fix warnings by awaiting async UI, not suppressing console.

## TypeScript JSX

Ensure `tsx` uses correct `jsx` compiler setting (`react-jsx`) in `tsconfig.json` for modern React.
