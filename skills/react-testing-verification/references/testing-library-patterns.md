# Testing Library Patterns

## Component Test Template

```tsx
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { OrderForm } from "./OrderForm";

it("submits order when quantity is valid", async () => {
  const user = userEvent.setup();
  const onSubmit = vi.fn();

  render(<OrderForm onSubmit={onSubmit} />);

  await user.type(screen.getByLabelText(/sku/i), "LP-100");
  await user.clear(screen.getByLabelText(/quantity/i));
  await user.type(screen.getByLabelText(/quantity/i), "2");
  await user.click(screen.getByRole("button", { name: /place order/i }));

  expect(onSubmit).toHaveBeenCalledWith({ sku: "LP-100", quantity: 2 });
});
```

## Async Data

```tsx
render(<OrdersPage />);
expect(await screen.findByRole("heading", { name: /orders/i })).toBeInTheDocument();
expect(await screen.findByText("ORD-001")).toBeInTheDocument();
```

## What Not to Test

- CSS class names for styling only
- That a specific hook was called — test rendered outcome instead
- Third-party library internals

## Provider Wrapper

```tsx
function renderWithProviders(ui: React.ReactElement) {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  return render(
    <QueryClientProvider client={queryClient}>{ui}</QueryClientProvider>,
  );
}
```

Reuse project helper if one exists — do not duplicate in every file.
