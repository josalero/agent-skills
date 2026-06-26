# Eval: Angular RxJS Patterns

## Prompt

Fix a component that subscribes inside `route.paramMap.subscribe` and never unsubscribes, causing duplicate HTTP calls and memory leaks when navigating between order IDs.

## Expected Agent Behavior

- Replaces with switchMap chain or async pipe
- Explains operator choice
- Adds error handling in stream
- Mentions takeUntilDestroyed if class subscribe remains
- Suggests test or manual navigation verification

## Failure Signals

- Adds Subscription array manual cleanup only without fixing nested subscribe
- Uses mergeMap for route param changes causing race
- Ignores error path
