# Flow and Channels

## Cold Flow for Single-Consumer Streams

```kotlin
fun eventsFor(orderId: String): Flow<OrderEvent> = flow {
    repository.stream(orderId).collect { emit(it) }
}.flowOn(Dispatchers.IO)
```

## Backpressure with Buffer and Conflate

Use `buffer`, `conflate`, or `debounce` when producers outpace consumers.

## Testing with Turbine

```kotlin
@Test
fun emitsStatusUpdates() = runTest {
    repository.events("o-1").test {
        assertEquals(OrderEvent.Created, awaitItem())
        awaitComplete()
    }
}
```

## Channel Pipelines

Prefer Flow for most service pipelines. Use channels when multiple producers/consumers need explicit handoff.
