# Breaking Changes

## Common Migration Fixes

### Hosting Model (Generic Host)

Modern ASP.NET Core uses minimal hosting:

```csharp
// Before — Startup.cs pattern (older templates)
public class Startup
{
    public void ConfigureServices(IServiceCollection services) { }
    public void Configure(IApplicationBuilder app) { }
}

// After — Program.cs
var builder = WebApplication.CreateBuilder(args);
builder.Services.AddControllers();
var app = builder.Build();
app.MapControllers();
app.Run();
```

Merge `Startup` into `Program.cs` or extension methods during upgrade.

### Authentication API Changes

```csharp
// JWT bearer — register and validate
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuer = true,
            ValidIssuer = builder.Configuration["Auth:Issuer"],
            ValidateAudience = true,
            ValidAudience = builder.Configuration["Auth:Audience"],
            ValidateLifetime = true,
            IssuerSigningKey = new SymmetricSecurityKey(
                Encoding.UTF8.GetBytes(builder.Configuration["Auth:SigningKey"]!))
        };
    });
```

Review Microsoft security advisories when bumping `Microsoft.AspNetCore.Authentication.*`.

### EF Core Query Breaking Changes

```csharp
// Client evaluation removed — push filter to SQL
var orders = await db.Orders
    .Where(o => o.CreatedAt >= cutoff) // translatable
    .ToListAsync(cancellationToken);

// If logic is not translatable, fetch then filter in memory explicitly and document why
```

After EF major bumps, run:

```bash
dotnet ef migrations add UpgradeToEf9 --project src/Infrastructure
```

Review generated migration for model snapshot diffs even when schema unchanged.

### Removed or Obsolete APIs

Search the solution after upgrade:

```bash
rg "Obsolete|CS0618|SYSLIB" --type cs
dotnet build 2>&1 | rg "error CS"
```

Replace patterns:

| Removed / obsolete | Replacement |
| --- | --- |
| `WebHost.CreateDefaultBuilder` | `WebApplication.CreateBuilder` |
| `IHostingEnvironment` | `IWebHostEnvironment` |
| `BinaryFormatter` | JSON, protobuf, or approved serializer |
| Sync `HttpClient` misuse | `IHttpClientFactory` |

### Nullable and Required Members

Enable nullable on upgrade if not already:

```xml
<Nullable>enable</Nullable>
```

Fix warnings at public API boundaries first — suppressions require justification.

## Package Conflict Resolution

When packages fail to restore:

```bash
dotnet list package --vulnerable --include-transitive
dotnet nuget why <PackageId>
```

Align transitive versions via central package management or explicit `PackageReference` overrides.

## Rollback Plan

- Keep migration commits small and tagged
- Maintain previous container image in registry for quick revert
- Document SDK/runtime pair that last passed production smoke tests

## Post-Migration Smoke Tests

- Health endpoints return 200
- Auth flow (login, token refresh) works
- Critical CRUD path with EF migration applied
- Background workers start and process test message
