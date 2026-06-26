# Angular CI Pipeline Gates

## Typical Scripts

```json
{
  "scripts": {
    "lint": "ng lint",
    "test:ci": "ng test --watch=false --browsers=ChromeHeadless --code-coverage",
    "build": "ng build --configuration=production",
    "check": "npm run lint && npm run test:ci && npm run build"
  }
}
```

Jest-based Angular projects use `jest --ci --coverage` instead of Karma — follow `package.json`.

## Example CI

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
```

ChromeHeadless requires Chrome/Chromium on runner — use `@angular/cli` documented CI images or install deps.

## PR vs Main

| Gate | PR | Main |
| --- | --- | --- |
| lint | Yes | Yes |
| unit tests + coverage | Yes | Yes |
| production build | Yes | Yes |
| e2e (`ng e2e`) | Optional | Nightly |

## Nx Monorepos

Use `nx run-many -t lint test build --projects=app-name` — document affected targets in CI.

## Related Skills

- `angular-performance` — bundle budget as optional gate in `angular.json`
- `testing-strategy` — e2e frequency
