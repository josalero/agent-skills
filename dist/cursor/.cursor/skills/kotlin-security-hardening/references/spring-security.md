# Spring Security for Kotlin Services

## Resource Server JWT

```kotlin
@Bean
fun securityFilterChain(http: HttpSecurity): SecurityFilterChain =
    http.authorizeHttpRequests { auth ->
        auth.requestMatchers("/actuator/health").permitAll()
            .anyRequest().authenticated()
    }
    .oauth2ResourceServer { it.jwt {} }
    .build()
```

## Method Security

```kotlin
@PreAuthorize("hasRole('ADMIN')")
fun deleteUser(id: UUID) { /* ... */ }
```

## CSRF and Sessions

Use stateless JWT for APIs; enable CSRF only for cookie-based browser sessions.
