# GC and Memory

## Common Kotlin/JVM Leak Sources

- Static caches without bounds
- Coroutine scopes not tied to lifecycle
- Classloader leaks in hot redeploy scenarios
- Listener registrations without removal

## GC Log Review

Look for increasing old-gen occupancy, frequent Full GC, or pause times exceeding SLO.

## Fix Pattern

1. Prove retention path with heap dump
2. Fix lifecycle or cache bounds
3. Re-measure with the same load test
