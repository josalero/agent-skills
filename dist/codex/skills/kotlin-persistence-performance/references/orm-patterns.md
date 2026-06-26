# ORM Patterns (JPA and Exposed)

## N+1 Detection

Enable Hibernate statistics or SQL logging temporarily. Look for repeated `select` per parent row.

## Fetch Joins and Entity Graphs

```kotlin
@Query("SELECT o FROM Order o JOIN FETCH o.lineItems WHERE o.id = :id")
fun findWithItems(id: UUID): Order?
```

## Exposed Projections

Prefer `slice` and explicit columns over loading full row objects for list endpoints.

## Batch Size

```yaml
spring.jpa.properties.hibernate.jdbc.batch_size: 50
spring.jpa.properties.hibernate.order_inserts: true
```
