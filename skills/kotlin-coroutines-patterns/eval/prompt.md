# Eval: Kotlin Coroutines Patterns

## Prompt

Our Spring Boot order service launches unstructured `GlobalScope` coroutines for payment and inventory calls. Requests time out under load and jobs keep running after the HTTP response completes. Refactor to structured concurrency with proper scopes, dispatchers, and cancellation.

## Expected Agent Behavior

- Replaces GlobalScope with request- or service-scoped coroutines
- Uses appropriate dispatchers for blocking vs suspend I/O
- Propagates cancellation and adds timeouts to external calls
- Adds coroutine tests with runTest

## Failure Signals

- Keeps fire-and-forget GlobalScope launches
- Blocks on Dispatchers.Default
- Swallows CancellationException
