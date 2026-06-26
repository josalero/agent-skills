---
name: frontend-ui-engineering
description: Implement and review frontend UI with semantic HTML, Tailwind CSS, responsive layouts, reusable patterns, and loading/empty/error states. Use when building pages, forms, dashboards, or fixing UI bugs in React, Angular, or static HTML projects.
---

# Frontend UI Engineering

## Workflow

1. Inspect stack — React, Angular, or static HTML; Tailwind version, component library, and existing layout primitives.
2. Read design tokens or Tailwind config — reuse spacing, color roles, and typography before adding utilities.
3. Structure with semantic HTML — landmarks, headings, lists, `button`/`a`, labels tied to inputs.
4. Build mobile-first layout — grid/flex, breakpoints, readable touch targets.
5. Implement all meaningful states — loading, empty, error, disabled — not happy-path only.
6. Keep components small; extract repeated Tailwind clusters into shared components or documented patterns.
7. Verify keyboard focus order, visible focus rings, and contrast on primary actions (coordinate with accessibility skills).
8. Run lint/build and spot-check responsive widths.

## References

- Read `references/semantic-html-and-layout.md` for landmarks, forms, and responsive patterns.
- Read `references/tailwind-patterns-and-states.md` for utility discipline, variants, and state UI.

## Quality Checklist

- No interactive `div`/`span` where `button` or `a` is correct.
- Form fields have visible labels; errors linked with `aria-describedby` when needed.
- Primary vs secondary actions visually distinct; destructive actions confirmed or styled consistently.
- No unexplained arbitrary Tailwind values — use scale tokens.
- Layout works at 320px and desktop without horizontal scroll on main content.
- Loading does not collapse layout (skeletons or min-height where appropriate).

## Output

Summarize:

- Files/components changed
- Layout and token decisions
- States implemented
- Accessibility notes deferred to follow-up if any
- Manual verification viewports and flows tested

## Related skills

- `ux-design-review` — flow and heuristic review before large UI work
- `ui-design-system-review` — token and component consistency audit
- `react-accessibility` / `angular-accessibility` — deep a11y fixes and ARIA patterns
- `react-component-engineering` — React-specific component architecture
