# Eval: Angular Performance

## Prompt

Typing in a filter box lags on a table with 3,000 rows. Default change detection is on. Diagnose and propose minimal fixes.

## Expected Agent Behavior

- Identifies change detection + template work as likely cause
- Recommends debounced filter, OnPush, track in @for, virtualization or pagination
- Mentions measuring with DevTools
- Avoids blanket OnPush without input immutability plan

## Failure Signals

- Suggests only upgrading Angular version
- Ignores trackBy/@for track
- Runs filter in template method without fix
