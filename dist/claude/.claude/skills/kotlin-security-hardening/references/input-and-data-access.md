# Input Validation and Data Access

## Boundary Validation

```kotlin
data class CreateUserRequest(
    @field:Email @field:NotBlank val email: String,
    @field:Size(min = 12) val password: String,
)
```

## Parameterized Queries

```kotlin
@Query("SELECT u FROM User u WHERE u.email = :email")
fun findByEmail(@Param("email") email: String): User?
```

Never build JPQL/SQL with string templates from user input.

## Safe Error Responses

Return ProblemDetail with generic messages to clients; log detailed causes server-side only.
