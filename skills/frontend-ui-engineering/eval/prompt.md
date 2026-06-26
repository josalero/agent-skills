# Eval: Frontend UI Engineering

## Prompt

Add a team settings page to our React + Tailwind app. Requirements: list members in a table on desktop, stacked cards on mobile, invite button, empty state when no members, loading skeleton on fetch, inline error if invite API fails. Use existing shadcn Button and Input components where possible.

Implement the UI structure and states. Do not wire a real API — use placeholder data and clear TODO for the fetch hook.

## Expected behavior

- Agent uses semantic structure (`main`, `h1`, `table` or accessible list pattern).
- Agent implements responsive layout (mobile cards, desktop table or responsive table pattern).
- Agent includes loading, empty, and error UI — not only populated happy path.
- Agent reuses design tokens / shadcn primitives — avoids one-off hex colors.
- Agent uses `button` for actions and associates form labels correctly.
