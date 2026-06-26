# Structured Concurrency

## Scope Ownership

Launch work from a scope that matches lifecycle — request scope in web apps, `SupervisorJob` when child failures should not cancel siblings.

```kotlin
class OrderProcessor(private val scope: CoroutineScope) {
    suspend fun process(orderId: String) = coroutineScope {
        val inventory = async { inventoryClient.reserve(orderId) }
        val payment = async { paymentClient.charge(orderId) }
        finalize(inventory.await(), payment.await())
    }
}
```

## Dispatcher Selection

| Work type | Dispatcher |
| --- | --- |
| CPU-bound computation | `Dispatchers.Default` |
| Blocking JDBC/files | `Dispatchers.IO` |
| UI (if applicable) | `Dispatchers.Main` |

## Cancellation

Do not catch `CancellationException`. Use `ensureActive()` in long loops.

```kotlin
suspend fun pollUntilReady(id: String) {
    while (currentCoroutineContext().isActive) {
        if (repository.isReady(id)) return
        delay(100)
    }
}
```
