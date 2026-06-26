# Containers and Health

## Multi-Stage Dockerfile

```dockerfile
FROM mcr.microsoft.com/dotnet/sdk:9.0 AS build
WORKDIR /src
COPY ["src/Api/Api.csproj", "Api/"]
COPY ["src/Infrastructure/Infrastructure.csproj", "Infrastructure/"]
RUN dotnet restore "Api/Api.csproj"
COPY src/ .
WORKDIR /src/Api
RUN dotnet publish "Api.csproj" -c Release -o /app/publish /p:UseAppHost=false

FROM mcr.microsoft.com/dotnet/aspnet:9.0 AS final
WORKDIR /app
RUN adduser --disabled-password --gecos "" appuser
USER appuser
COPY --from=build /app/publish .
ENV ASPNETCORE_URLS=http://+:8080
EXPOSE 8080
ENTRYPOINT ["dotnet", "Api.dll"]
```

Use `/p:UseAppHost=false` for container-friendly single-file entry via `dotnet`.

## Health Checks

```csharp
builder.Services.AddHealthChecks()
    .AddNpgSql(builder.Configuration.GetConnectionString("Default")!,
        name: "postgres",
        tags: ["ready"])
    .AddCheck("self", () => HealthCheckResult.Healthy(), tags: ["live"]);

var app = builder.Build();

app.MapHealthChecks("/health/live", new HealthCheckOptions
{
    Predicate = check => check.Tags.Contains("live")
});

app.MapHealthChecks("/health/ready", new HealthCheckOptions
{
    Predicate = check => check.Tags.Contains("ready")
});
```

| Probe | Endpoint | Purpose |
| --- | --- | --- |
| Liveness | `/health/live` | Process is running — restart if fails |
| Readiness | `/health/ready` | Ready for traffic — includes DB |

Do not put dependency checks on liveness unless you want restarts when downstream blips.

## Graceful Shutdown

```csharp
builder.Services.Configure<HostOptions>(options =>
{
    options.ShutdownTimeout = TimeSpan.FromSeconds(30);
});

builder.WebHost.ConfigureKestrel(options =>
{
    options.Limits.KeepAliveTimeout = TimeSpan.FromMinutes(2);
});
```

Kubernetes `terminationGracePeriodSeconds` must exceed in-flight request drain time.

## Local Container Run

```bash
docker build -t orders-api:local .
docker run --rm -p 8080:8080 \
  -e ASPNETCORE_ENVIRONMENT=Development \
  -e ConnectionStrings__Default="Host=host.docker.internal;..." \
  orders-api:local

curl -f http://localhost:8080/health/ready
```

Use double underscore for nested configuration keys in environment variables.

## Container Checklist

- `.dockerignore` excludes `bin/`, `obj/`, and secrets
- Non-root user in final stage
- No `ASPNETCORE_ENVIRONMENT=Production` secrets in Dockerfile `ENV`
- Published output only in final layer — no SDK in runtime image
