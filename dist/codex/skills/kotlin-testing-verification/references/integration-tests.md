# Integration Tests

## Spring Boot Slice

```kotlin
@WebMvcTest(OrderController::class)
class OrderControllerTest { /* MockMvc tests */ }
```

## Testcontainers

```kotlin
@Testcontainers
@SpringBootTest
class OrderRepositoryIT {
    companion object {
        @Container
        val postgres = PostgreSQLContainer("postgres:16")
    }
}
```

## CI Commands

```bash
./gradlew test
./gradlew integrationTest  # if separated
```
