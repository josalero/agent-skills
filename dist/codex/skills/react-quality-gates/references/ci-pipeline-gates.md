# React CI Pipeline Gates

## Typical package.json Scripts

```json
{
  "scripts": {
    "lint": "eslint src --max-warnings 0",
    "format:check": "prettier --check \"src/**/*.{ts,tsx,css,md}\"",
    "typecheck": "tsc --noEmit",
    "test:ci": "vitest run --coverage",
    "check": "npm run lint && npm run format:check && npm run typecheck && npm run test:ci",
    "build": "vite build"
  }
}
```

Use `npm run check` as the single CI entry when possible.

## Example GitHub Actions

```yaml
jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "22"
          cache: npm
      - run: npm ci
      - run: npm run check
      - run: npm run build
```

## PR vs Main

| Gate | PR | Main |
| --- | --- | --- |
| lint + format + typecheck | Yes | Yes |
| unit tests + coverage | Yes | Yes |
| production build | Yes | Yes |
| E2E (Playwright/Cypress) | Optional | Nightly |

## Monorepo Notes

Run gates per package with filters (`npm run check -w fe`) — document which workspace CI targets.

## Husky (local gate)

Pre-commit hooks complement CI — they do not replace CI. Keep hooks fast (lint-staged).

## Related Skills

- `react-performance` — bundle size budgets optional as advisory gate
- `testing-strategy` — E2E placement
