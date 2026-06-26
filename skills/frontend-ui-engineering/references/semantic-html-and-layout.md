# Semantic HTML and Layout

## Page shell

```html
<body>
  <a href="#main" class="sr-only focus:not-sr-only …">Skip to content</a>
  <header>…</header>
  <nav aria-label="Primary">…</nav>
  <main id="main">…</main>
  <footer>…</footer>
</body>
```

Use one `h1` per view; heading levels do not skip levels for styling convenience.

## Forms

```html
<label for="email">Email</label>
<input id="email" name="email" type="email" autocomplete="email" required />
<p id="email-error" role="alert">…</p>
```

Associate errors with `aria-describedby="email-error"` when inline validation is shown.

## Responsive layout patterns

- **Stack → row**: `flex flex-col gap-4 md:flex-row md:items-center`
- **Sidebar layout**: grid `grid-cols-1 lg:grid-cols-[240px_1fr]` or flex with `shrink-0` nav
- **Card grid**: `grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4`
- **Page max width**: `mx-auto w-full max-w-6xl px-4 sm:px-6`

## Framework notes

- **React**: prefer semantic elements in JSX; pass `className` to shared primitives.
- **Angular**: use native control flow; bind `class` on host or template with same Tailwind patterns.
- Avoid wrapper `div` soup — use `section`, `article`, `ul`/`li` where they match content.
