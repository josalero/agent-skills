# Unit Tests in Kotlin

## JUnit 5 with MockK

```kotlin
@Test
fun `applies discount when code is SAVE10`() {
    val service = DiscountService()
    val total = service.apply(listOf(LineItem(BigDecimal("10"), 2)), "SAVE10")
    assertEquals(BigDecimal("18.00"), total)
}
```

## Naming

Use backtick names or `should_expectedBehavior_when_condition` style consistently with the project.

## Coroutine Unit Tests

```kotlin
@Test
fun completesWithinTimeout() = runTest {
    val result = service.fetchStatus("o-1")
    assertEquals(Status.READY, result)
}
```
