# Eval: React AI Product Engineering

## Prompt

Implement a chat widget in React for a product catalog assistant. Answers stream from POST `/api/v1/chat/stream`. Show citations when provided. Handle stop, error, and empty states. Must be keyboard accessible.

## Expected Agent Behavior

- Proposes hook + presentational components with streaming append
- Includes cancel via AbortController and stop button
- Sanitizes markdown output; renders source links
- Uses aria-live politely; documents Enter/Shift+Enter behavior
- Covers loading/error/empty UI states explicitly

## Failure Signals

- dangerouslySetInnerHTML for model output
- No stop/cancel during stream
- Missing citation UI when API returns sources
- No keyboard or screen reader consideration
