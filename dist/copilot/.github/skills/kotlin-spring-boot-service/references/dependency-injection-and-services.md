# Dependency Injection and Services

## Constructor Injection

```kotlin
@Service
class OrderService(
    private val repository: OrderRepository,
    private val clock: Clock,
) {
    @Transactional
    fun create(request: CreateOrderRequest): Order { /* ... */ }
}
```

## Layering

- Controllers: HTTP translation only
- Services: business rules and transaction boundaries
- Repositories: persistence access

## Coroutines in Spring

Use `suspend` controller methods with structured scopes when mixing coroutines and Spring MVC/WebFlux. Keep blocking JDBC on `Dispatchers.IO` when not using R2DBC.

## Testing

- Unit test services with mocked repositories
- `@WebMvcTest` for controller contract and validation
- `@DataJpaTest` or Testcontainers when persistence behavior matters
