# Auth and Validation

## JWT Middleware (Axum)

Validate issuer, audience, and expiry before inserting claims into request extensions.

## Request Validation

```rust
#[derive(Deserialize, Validate)]
struct CreateUserRequest {
    #[validate(email)]
    email: String,
    #[validate(length(min = 12))]
    password: String,
}
```

## Rate Limiting

Apply tower-governor or similar at edge for auth and write endpoints.

## Principle of Least Privilege

Scope API keys and JWT claims to minimum required actions.
