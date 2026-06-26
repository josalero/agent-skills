# Angular Lint, Build, and Coverage

## angular-eslint

```json
{
  "eslintConfig": {
    "extends": [
      "plugin:@angular-eslint/recommended",
      "plugin:@angular-eslint/template/process-inline-templates"
    ]
  }
}
```

Run via `ng lint` or flat config equivalent — align with Angular major version.

## Strict TypeScript and Templates

```json
{
  "angularCompilerOptions": {
    "strictTemplates": true,
    "strictInjectionParameters": true,
    "strictInputAccessModifiers": true
  },
  "compilerOptions": {
    "strict": true
  }
}
```

Enable flags one at a time on legacy apps — fix template type errors, not `$any()` everywhere.

## Prettier

Use `@angular-eslint/template-parser` compatibility — format HTML templates with Prettier Angular plugin when adopted.

## Karma Coverage (angular.json excerpt)

```json
"test": {
  "options": {
    "codeCoverage": true,
    "codeCoverageExclude": [
      "src/**/*.module.ts",
      "src/main.ts",
      "src/environments/**"
    ]
  }
}
```

Enforce thresholds in `karma.conf.js`:

```javascript
coverageReporter: {
  check: {
    global: {
      statements: 70,
      branches: 60,
      functions: 70,
      lines: 70
    }
  }
}
```

## Jest (Angular)

Use `jest-preset-angular` coverageThreshold — same ratchet principles.

## Production Build Gate

`ng build --configuration=production` catches:

- Template type errors missed in dev
- Budget violations (if configured)
- AOT compilation failures

Do not rely on `ng serve` alone before merge.

## Fixing Failures

| Issue | Approach |
| --- | --- |
| Template strict error | Fix component API or narrow union type |
| Karma CI flake | Increase timeouts; remove real timers without fakeAsync |
| ESLint component selector | Match project prefix rule |
| Budget exceeded | Lazy load or adjust budget with architect approval |

## Related Skills

- `angular-testing-verification` — stable unit tests
- `angular-accessibility` — template a11y lint rules when enabled
