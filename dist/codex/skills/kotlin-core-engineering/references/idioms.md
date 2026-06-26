# Kotlin Idioms and Patterns

Prefer clarity over cleverness. Match the project's Kotlin version and compiler settings before introducing newer language features.

## Data Classes for Immutable Value Objects

Use data classes for stable, read-only carriers with clear equality semantics.

```kotlin
data class MoneyAmount(val value: BigDecimal, val currency: Currency) {
    init {
        require(value.signum() >= 0) { "value must be non-negative" }
    }
}
```

## Sealed Types for Exhaustive Domain Modeling

Use sealed hierarchies when a closed set of variants is a business rule.

```kotlin
sealed interface PaymentResult
data class PaymentAccepted(val authorizationId: String) : PaymentResult
data class PaymentDeclined(val reasonCode: String) : PaymentResult
data class PaymentPending(val reference: String) : PaymentResult

fun messageFor(result: PaymentResult): String = when (result) {
    is PaymentAccepted -> "Accepted: ${result.authorizationId}"
    is PaymentDeclined -> "Declined: ${result.reasonCode}"
    is PaymentPending -> "Pending: ${result.reference}"
}
```

## Null Safety at Boundaries

Prefer non-null types in domain models. Use nullable types only where absence is meaningful.

```kotlin
fun findByEmail(email: String): User? = repository.findByEmail(email)

fun requireUser(email: String): User =
    findByEmail(email) ?: throw UserNotFoundException(email)
```

## Intentional Scope Functions

Use `let`, `run`, `apply`, and `also` to reduce noise — not to chain unrelated side effects.

```kotlin
fun normalize(input: String?): String =
    input?.trim()?.lowercase().orEmpty()
```

## Intentional Exceptions

Catch specific exceptions. Preserve cause. Do not swallow.

```kotlin
fun loadInvoice(id: UUID): Invoice = try {
    repository.findById(id) ?: throw InvoiceNotFoundException(id)
} catch (ex: DataAccessException) {
    throw InvoiceLoadException("Failed to load invoice $id", ex)
}
```
