# Eval: Angular Application Engineering

## Prompt

Split a 350-line `DashboardComponent` that loads data, formats dates, and renders tables/filters. Use standalone components and match existing Angular patterns in the repo.

## Expected Agent Behavior

- Extracts presentational components and injects services
- Uses OnPush where appropriate with async pipe or signals
- Handles loading/error states
- Preserves routing and does not mass-migrate unrelated NgModules
- Lists verification command (`ng test`, `npm test`)

## Failure Signals

- Everything moved to one giant service without UI split
- Subscriptions leak without cleanup pattern
- Breaks accessibility on buttons/forms
