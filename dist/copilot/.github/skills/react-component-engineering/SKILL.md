---
name: react-component-engineering
description: Build and review React components with clear boundaries, props, state ownership, composition, and maintainable rendering. Use when creating UI components, refactoring prop drilling, splitting large components, or improving readability and testability in React apps.
---

# React Component Engineering

## Workflow

1. Inspect React version, UI library (Ant Design, shadcn, MUI), styling approach (Tailwind, CSS modules), and existing component patterns.
2. Identify component type: presentational, container, form, layout, or page — and who owns data fetching.
3. Keep components focused: one primary responsibility; extract when JSX or logic becomes hard to scan.
4. Define explicit props types; avoid boolean prop explosion — prefer composition or variants.
5. Colocate state at the lowest owner that needs it; lift only when siblings must share it.
6. Prefer semantic HTML and accessible patterns before custom widgets.
7. Verify with component tests and Storybook or manual states (loading, empty, error) when applicable.

## References

- Read `references/component-patterns.md` for composition, props, and container/presentational split.
- Read `references/rendering-and-performance-basics.md` for keys, lists, conditional render, and memo discipline.

## Quality Checklist

- Props interface is typed and documents required vs optional behavior.
- No business logic hidden in presentational components.
- Event handlers named `on*`; callbacks do not mutate props.
- Lists use stable keys — not array index for mutable data.
- Loading, empty, and error states are handled explicitly.
- Components are testable without mounting the entire app.

## Output

After component work, summarize:

- Components created or split
- State ownership decisions
- Props/public API of exported components
- Tests or stories added
- Follow-up refactors deferred intentionally
