# Forms and Semantics

## Label Association

```tsx
<label htmlFor="email" className="block text-sm font-medium">
  Email
  <input
    id="email"
    name="email"
    type="email"
    autoComplete="email"
    aria-invalid={errors.email ? true : undefined}
    aria-describedby={errors.email ? "email-error" : undefined}
    className="mt-1 w-full rounded border px-3 py-2"
  />
</label>
{errors.email ? (
  <p id="email-error" role="alert" className="mt-1 text-sm text-red-700">
    {errors.email}
  </p>
) : null}
```

## Page Landmarks

```tsx
<a href="#main" className="sr-only focus:not-sr-only">
  Skip to main content
</a>
<header>...</header>
<nav aria-label="Primary">...</nav>
<main id="main">...</main>
<footer>...</footer>
```

## Heading Hierarchy

One `h1` per page view; do not skip levels for styling — use CSS for visual size.

## Button vs Link

- `button` for actions on current page (submit, open modal)
- `a href` for navigation to new URL

```tsx
// Wrong
<div onClick={save}>Save</div>

// Right
<button type="button" onClick={save}>Save</button>
```

## Images

```tsx
<img src={product.imageUrl} alt={product.name} />
<img src="/icons/search.svg" alt="" aria-hidden="true" />
```

Decorative images: empty alt or `aria-hidden`.
