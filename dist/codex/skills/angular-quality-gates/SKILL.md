---
name: angular-quality-gates
description: Configure and fix Angular CI quality gates. Use when setting up or repairing ng build, ng test, ESLint with angular-eslint, Prettier, strict template type checking, Karma or Jest CI runs, coverage thresholds, or pipeline failures on lint, typecheck, or unit tests.
---

# Angular Quality Gates

## Workflow

1. Read `angular.json`, `package.json`, `tsconfig.json` (app + spec), ESLint config, and CI workflow.
2. Identify gate commands — commonly `npm run lint`, `npm run test:ci`, `ng build --configuration=production`.
3. Read `references/ci-pipeline-gates.md` for CI layout.
4. Read `references/lint-build-and-coverage.md` for angular-eslint, strict templates, and coverage.
5. Enable strict template checking incrementally — fix component TS and templates together.
6. Prefer `ng test --watch=false --browsers=ChromeHeadless` (Karma) or Jest preset per project — match CI.
7. Run the same scripts locally as CI after `npm ci`.

## Gate Checklist

- Production build succeeds (`ng build` or `npm run build`).
- ESLint (`ng lint` or `eslint`) passes with zero errors on PR.
- Unit tests pass headless in CI.
- Strict templates and `strict` TypeScript honored in changed code.
- Coverage thresholds set in Karma/Jest config for `src/app` logic — not module stubs only.

## Output

Summarize gate scripts, CI jobs, config files, verification commands, deferred strictness work.

## Related Skills

- `angular-testing-verification` — TestBed and component tests
- `testing-strategy` — CI layering
- `angular-application-engineering` — feature fixes
