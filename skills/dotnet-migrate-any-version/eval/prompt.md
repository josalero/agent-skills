# Eval: .NET Migrate Any Version

## Prompt

Upgrade a solution from .NET 8 to .NET 9. Projects: `Api`, `Infrastructure`, `Domain`, `Api.Tests`. Uses EF Core 8, ASP.NET Core 8, GitHub Actions with `dotnet-version: 8.0.x`, and Docker `aspnet:8.0`. Provide an ordered migration plan and the first concrete file changes.

## Expected Agent Behavior

- Inventories current TFMs, packages, global.json, CI, and Docker tags
- Upgrades SDK/TFM before fixing source; aligns Microsoft.* package majors
- Mentions running `dotnet build` and `dotnet test` after each step
- Updates CI and Docker base images to 9.0
- Calls out EF migration review and WebApplicationFactory test verification
- Summarizes rollback approach

## Failure Signals

- Changes random NuGet packages without aligning ASP.NET/EF versions
- Skips CI or container updates
- Single giant step with no incremental verification
- Ignores breaking change search (`dotnet build` errors)
