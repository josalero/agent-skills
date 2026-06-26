# Tailwind Patterns and States

## Utility discipline

- Prefer design tokens: `bg-primary text-primary-foreground` over raw palette utilities in features.
- Group related utilities logically: layout → spacing → typography → color → state.
- Extract the fourth copy of the same class string into a component — not before.

## Button pattern (example)

```html
<button
  type="button"
  class="inline-flex items-center justify-center rounded-md px-4 py-2 text-sm font-medium
         bg-primary text-primary-foreground hover:bg-primary/90
         focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring
         disabled:pointer-events-none disabled:opacity-50"
>
  Save
</button>
```

## State UI

| State | Pattern |
| --- | --- |
| Loading | Disable control + spinner or skeleton; preserve button width |
| Empty | Illustration optional; heading + explanation + primary CTA |
| Error (page) | Heading, short explanation, retry + support link |
| Error (inline) | Text under field; summarize at form top for submit failures |

## Skeleton example

```html
<div class="animate-pulse space-y-3" aria-busy="true" aria-label="Loading content">
  <div class="h-4 w-3/4 rounded bg-muted"></div>
  <div class="h-4 w-1/2 rounded bg-muted"></div>
</div>
```

Replace with real content and remove `aria-busy` when loaded.

## Dark mode

When the project supports dark mode, use token pairs (`bg-background text-foreground`) that flip with `dark:` or CSS variables — avoid hardcoding separate gray scales per theme in feature code.
