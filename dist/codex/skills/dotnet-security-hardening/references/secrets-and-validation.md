# Secrets and Validation

## Configuration and Secrets

```csharp
// appsettings.json — placeholders only, no real secrets
{
  "ConnectionStrings": {
    "Default": "" 
  },
  "Auth": {
    "SigningKey": ""
  }
}

// Program.cs — production values from environment or Key Vault
builder.Configuration.AddEnvironmentVariables();

if (!builder.Environment.IsDevelopment())
{
    builder.Configuration.AddAzureKeyVault(
        new Uri(builder.Configuration["KeyVault:Uri"]!),
        new DefaultAzureCredential());
}
```

User secrets for local dev only:

```bash
dotnet user-secrets set "Auth:SigningKey" "<dev-only-key>" --project src/Api
```

Never commit `appsettings.Production.json` with real credentials.

## Input Validation

```csharp
public sealed record CreateUserRequest
{
    [Required]
    [EmailAddress]
    [MaxLength(256)]
    public required string Email { get; init; }

    [Required]
    [MinLength(12)]
    [MaxLength(128)]
    public required string Password { get; init; }
}
```

For complex rules, use FluentValidation:

```csharp
public sealed class CreateUserRequestValidator : AbstractValidator<CreateUserRequest>
{
    public CreateUserRequestValidator()
    {
        RuleFor(x => x.Email).NotEmpty().EmailAddress().MaximumLength(256);
        RuleFor(x => x.Password).MinimumLength(12).MaximumLength(128);
    }
}
```

Validate at the API boundary; re-validate invariants in domain code when security-critical.

## Parameterized Data Access

```csharp
// Avoid — SQL injection
var sql = $"SELECT * FROM Orders WHERE CustomerEmail = '{email}'";
await db.Database.ExecuteSqlRawAsync(sql);

// Prefer — parameterized
await db.Orders
    .Where(o => o.CustomerEmail == email)
    .ToListAsync(cancellationToken);

// Raw SQL when needed
await db.Database.ExecuteSqlAsync(
    $"DELETE FROM Sessions WHERE ExpiresAt < {{0}}",
    DateTimeOffset.UtcNow);
```

## Safe Logging and Errors

```csharp
// Avoid
logger.LogInformation("Login failed for {Email} with password {Password}", email, password);

// Prefer
logger.LogWarning("Login failed for user {UserId}", userId);
```

Production exception handler:

```csharp
ProblemDetails problem = exception switch
{
    ValidationException ex => new ValidationProblemDetails(/* ... */),
    _ => new ProblemDetails
    {
        Status = StatusCodes.Status500InternalServerError,
        Title = "An error occurred",
        Detail = app.Environment.IsDevelopment() ? exception.Message : null
    }
};
```

Do not return stack traces or inner exception details to external clients in production.

## Dependency Vulnerabilities

```bash
dotnet list package --vulnerable --include-transitive
```

Upgrade or mitigate critical CVEs; document accepted risk with expiry when upgrade is blocked.

## Secrets Checklist

- No secrets in git history, logs, URLs, or client-side storage
- Connection strings and API keys rotated after exposure
- PII minimized in logs — use opaque user ids
- File uploads validated for size, type, and stored outside web root
