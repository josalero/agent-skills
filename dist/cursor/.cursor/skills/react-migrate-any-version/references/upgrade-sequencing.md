# Upgrade Sequencing

## Recommended Order

```text
1. Node.js to supported LTS for target toolchain
2. Bundler (Vite/webpack) and TypeScript
3. react + react-dom (same exact version)
4. @types/react + @types/react-dom
5. Router, Query, UI libraries (one at a time if brittle)
6. Test stack (@testing-library/*, vitest/jest)
7. Application code fixes + codemods
```

## Package Upgrade Commands

```bash
npm install react@19 react-dom@19
npm install -D @types/react@19 @types/react-dom@19
npm dedupe
npm test -- --run
npm run build
```

Use project's package manager (pnpm/yarn) consistently.

## Peer Dependency Conflicts

- Check UI libraries for React 19 compatibility before bumping
- Use `npm ls react` to detect duplicate React copies (breaks hooks)
- Resolve with overrides/resolutions only as temporary bridge — document why

## Incremental PR Strategy

| PR | Scope |
| --- | --- |
| 1 | Tooling + React bump + mechanical fixes |
| 2 | Router/API migrations |
| 3 | Remove deprecated patterns and dead code |

Each PR keeps main deployable when possible.

## Verify Runtime

```bash
npm run dev
npm run preview   # production build locally
```

Smoke critical routes manually after preview build.
