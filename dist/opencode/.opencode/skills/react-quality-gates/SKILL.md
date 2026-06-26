---
name: react-quality-gates
description: Configure and fix React frontend CI quality gates. Use when setting up or repairing npm lint, format check, TypeScript build, Vitest or Jest with coverage thresholds, Husky pre-commit hooks, or GitHub Actions failures on ESLint, Prettier, tsc, or test scripts.
---

# React Quality Gates

## Workflow

1. Read `package.json` scripts, ESLint config (`eslint.config.js` or `.eslintrc`), Prettier, `tsconfig.json`, Vitest/Jest config, and CI workflow.
2. Identify the **CI gate script** — often `npm run check`, `lint`, `test:ci`, or `build`.
3. Read `references/ci-pipeline-gates.md` for pipeline structure.
4. Read `references/lint-typecheck-and-coverage.md` for ESLint, TypeScript, and coverage setup.
5. Fix type errors before relaxing `strict` — avoid `@ts-ignore` in changed files.
6. Keep ESLint and Prettier boundaries clear — use `eslint-config-prettier` to avoid rule fights.
7. Run the same npm script locally as CI (`npm ci` then gate script).

## Gate Checklist

- `tsc --noEmit` or `npm run build` passes with strict TypeScript when enabled.
- ESLint passes with zero errors on PR (warnings per team policy).
- Prettier check (`prettier --check`) or format gate passes.
- Unit tests pass in CI with stable `jsdom` / `happy-dom` environment.
- Coverage thresholds configured in Vitest/Jest — scoped to `src/`, not trivial files only.

## Output

Summarize scripts, CI config, threshold changes, commands (`npm run …`), and intentional exclusions.

## Related Skills

- `react-testing-verification` — Testing Library patterns
- `testing-strategy` — pyramid and flaky test policy
- `react-component-engineering` — component fixes
