# React Lint, Typecheck, and Coverage

## ESLint (flat config example)

```javascript
// eslint.config.js
import js from "@eslint/js";
import tseslint from "typescript-eslint";
import reactHooks from "eslint-plugin-react-hooks";

export default tseslint.config(
  js.configs.recommended,
  ...tseslint.configs.recommended,
  {
    plugins: { "react-hooks": reactHooks },
    rules: {
      "react-hooks/rules-of-hooks": "error",
      "react-hooks/exhaustive-deps": "warn",
    },
  }
);
```

Extend existing project config — do not replace with a generic preset mid-repo.

## TypeScript

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "skipLibCheck": true
  }
}
```

CI should run `tsc --noEmit` even when Vite build skips type errors (`vite build` alone is not enough).

## Prettier

```bash
npx prettier --check "src/**/*.{ts,tsx}"
npx prettier --write "src/**/*.{ts,tsx}"
```

Add `eslint-config-prettier` to disable conflicting ESLint stylistic rules.

## Vitest Coverage

```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    coverage: {
      provider: "v8",
      thresholds: {
        lines: 70,
        functions: 70,
        branches: 60,
      },
      include: ["src/**/*.{ts,tsx}"],
      exclude: ["src/**/*.d.ts", "src/main.tsx"],
    },
  },
});
```

Raise thresholds gradually; exclude only generated or barrel files.

## Jest Equivalent

Use `coverageThreshold` in `jest.config` — same principles as Vitest.

## Fixing Common CI Failures

| Issue | Fix |
| --- | --- |
| ESLint OOM | Lint scoped paths; enable cache |
| flaky timer tests | `vi.useFakeTimers()` with cleanup |
| path alias not resolved | Align `tsconfig paths` with Vitest `resolve.alias` |
| coverage drop on UI-only change | Test behavior; do not delete assertions |

## Related Skills

- `react-testing-verification` — user-centric tests
- `react-accessibility` — optional a11y ESLint plugins as advisory then blocking
