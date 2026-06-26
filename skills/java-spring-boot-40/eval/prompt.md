# Eval: Java Spring Boot 4.0

## Prompt

Plan and execute migration of a Spring Boot 3.5 / Java 21 monolith to Spring Boot 4.0. The app uses Spring Security OAuth2 resource server, Jackson for REST DTOs, and Hibernate/JPA. Produce a migration sequence, then bump the BOM and fix compile errors in Security and JSON tests.

## Expected Agent Behavior

- Confirms 3.5 baseline and Java 17+ before targeting 4.0
- Separates planning (risk areas, PR order) from implementation when asked
- Addresses Jackson 3 and Security 7 explicitly
- Uses `SecurityFilterChain`, not deprecated adapter patterns
- Runs `./gradlew check` or `mvn verify` and reports results
- Mentions JSpecify and Hibernate 7 as areas to verify

## Failure Signals

- Migrates from Boot 3.3 directly without noting 3.5 intermediate step
- Only bumps version without fixing Jackson or Security compile failures
- Reintroduces `javax.*` imports
- Assumes Undertow still works
- Skips tests after dependency upgrade
