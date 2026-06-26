---
name: angular-application-engineering
description: Build and review Angular applications with standalone components, services, routing, forms, and maintainable module boundaries. Use when implementing features, refactoring Angular structure, or aligning with modern Angular patterns in existing apps.
---

# Angular Application Engineering

## Workflow

1. Inspect Angular version, standalone vs NgModule usage, routing style, state approach, and UI library (Material, PrimeNG, etc.).
2. Identify feature boundaries: smart/container vs presentational components, services, and API clients.
3. Prefer standalone components and explicit imports unless the repo standardizes NgModules.
4. Keep templates readable — extract subcomponents and pipes instead of large HTML blocks.
5. Use typed reactive forms or typed template-driven patterns consistent with the project.
6. Route lazily for feature areas; guard auth routes on server-backed rules too.
7. Verify with component tests and `ng test` / `npm test` scoped to changed projects.

## References

- Read `references/components-and-services.md` for standalone components, DI, and smart/dumb split.
- Read `references/routing-and-forms.md` for lazy routes, guards, and reactive forms patterns.

## Checklist

- Components have single clear responsibility.
- Services encapsulate HTTP and business orchestration — not templates.
- Subscriptions cleaned up (`takeUntilDestroyed`, `async` pipe, or finite streams).
- API types/interfaces explicit; avoid `any` at boundaries.
- Error and loading states handled in UI.
- Public API of feature folders exported via barrel `index.ts` when repo uses them.

## Output

Summarize structure changes, components/services added, routing impact, tests run, and deferred refactors.
