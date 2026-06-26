# MSW and Hook Testing

## MSW Handler Example

```tsx
import { http, HttpResponse } from "msw";
import { setupServer } from "msw/node";

const server = setupServer(
  http.get("/api/v1/orders", () =>
    HttpResponse.json({ items: [{ id: "ORD-001", status: "OPEN" }] })),
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

Override per test for error paths:

```tsx
server.use(
  http.get("/api/v1/orders", () => HttpResponse.json({ message: "fail" }, { status: 500 })),
);
```

## Testing Custom Hooks

Use `@testing-library/react` `renderHook`:

```tsx
const { result } = renderHook(() => useDebouncedValue("abc", 300), {
  wrapper: QueryWrapper,
});

await waitFor(() => expect(result.current).toBe("abc"));
```

## Form Validation Tests

Assert visible error messages:

```tsx
await user.click(screen.getByRole("button", { name: /save/i }));
expect(await screen.findByText(/quantity must be at least 1/i)).toBeInTheDocument();
```

## CI Commands

```bash
npm test -- --run src/features/orders
npm run test:coverage -- --run
```

Match scripts in `package.json` — do not invent commands.
