# Eval: React Migrate Any Version

## Prompt

Plan migration from React 17 + CRA + React Router v5 to React 19 + Vite + React Router v6. Repo has 80 routes and Jest tests. Outline phased PRs and risk mitigations.

## Expected Agent Behavior

- Sequences tooling before app-wide codemods
- Calls out duplicate React, Strict Mode, router API changes, test migration
- Proposes incremental PRs with verification gates
- Mentions preview/smoke and rollback via branch deploy

## Failure Signals

- Single big-bang PR recommendation only
- Skips test and build verification steps
- Upgrades router before bundler without rationale
