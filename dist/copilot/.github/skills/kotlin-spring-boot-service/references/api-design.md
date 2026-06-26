# API Design for Kotlin Spring Boot

## Controller Boundaries

```kotlin
@RestController
@RequestMapping("/api/v1/orders")
class OrderController(private val service: OrderService) {
    @PostMapping
    fun create(@Valid @RequestBody request: CreateOrderRequest): OrderResponse =
        service.create(request).toResponse()
}
```

## DTOs and Validation

Use immutable data classes with Jakarta validation annotations at the edge.

```kotlin
data class CreateOrderRequest(
    @field:NotBlank val customerId: String,
    @field:NotEmpty val lineItems: List<LineItemRequest>,
)
```

## ProblemDetail Errors

Map domain exceptions to `ProblemDetail` in a single `@ControllerAdvice` handler.

## Pagination

Return stable page DTOs with cursor or offset metadata — never expose raw `Page<Entity>` types.
