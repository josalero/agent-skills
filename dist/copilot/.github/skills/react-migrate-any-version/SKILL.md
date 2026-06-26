---
name: react-migrate-any-version
description: Plan and execute React and ecosystem migrations across major versions, routers, build tools, and testing libraries. Use when upgrading React, migrating from CRA to Vite, updating React Router, or modernizing TypeScript and ESLint configs tied to React upgrades.
---

# React Migrate Any Version

## Workflow

1. Inventory current versions: React, React DOM, router, state libraries, test stack, bundler, and TypeScript.
2. Read official migration guides for target versions — note breaking changes and codemods.
3. Upgrade in layers: tooling (Node, bundler) → React core → ecosystem packages → app code fixes.
4. Run codemods where available; fix type errors and deprecated APIs incrementally.
5. Run test suite and key E2E flows after each layer; do not batch all fixes blindly.
6. Update CI and lockfile together; document peer dependency resolutions.
7. Ship behind flag or branch if migration spans multiple PRs.

## References

- Read `references/upgrade-sequencing.md` for order of operations and dependency alignment.
- Read `references/breaking-changes-checklist.md` for common React 18/19 and router migration items.

## Checklist

- React and React DOM versions match.
- `createRoot` used instead of legacy `ReactDOM.render`.
- Strict Mode behavior understood for double effects in dev.
- Router v6+ patterns (`Routes`, `Route`, hooks) applied consistently.
- Tests updated for async APIs and act warnings resolved properly.
- Build and lint pass in CI with frozen lockfile.

## Output

Summarize version delta, upgrade steps executed, breaking fixes, verification commands, and deferred follow-ups.
