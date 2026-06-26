# Eval: React Component Engineering

## Prompt

Refactor a 280-line `DashboardPage.tsx` that fetches data, formats currency, and renders tables and filters inline. Split into maintainable components following project conventions.

## Expected Agent Behavior

- Extracts presentational components and a data hook or container
- Preserves behavior; types props explicitly
- Handles loading/error/empty states in clear components
- Avoids unnecessary global state
- Summarizes component tree and ownership

## Failure Signals

- Creates 10 one-line wrapper files without purpose
- Moves everything to Context unnecessarily
- Breaks accessibility on buttons/links
- No tests or verification mention
