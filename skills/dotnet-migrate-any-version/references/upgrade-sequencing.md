# Upgrade Sequencing

## Pre-Flight Inventory

Collect before changing anything:

```bash
dotnet --version
grep -r TargetFramework *.csproj
dotnet list package --outdated
```

Document: target frameworks, central package management (`Directory.Packages.props`), global.json SDK pin, CI `actions/setup-dotnet` or equivalent version, Docker `FROM mcr.microsoft.com/dotnet/aspnet:*` tag.

## Recommended Order

1. **Update global.json SDK** to the target SDK (or band compatible with target runtime)
2. **Update TargetFramework** in all projects (`net8.0` → `net9.0`)
3. **Align Microsoft.* packages** — ASP.NET Core, EF Core, Extensions share a major version
4. **Fix compile errors** from breaking changes (search build log, fix project by project)
5. **Run full test suite** and fix test host / WebApplicationFactory breaks
6. **Update CI and containers** to matching SDK/runtime images
7. **Deploy to staging** with smoke tests before production

## Project File Changes

```xml
<PropertyGroup>
  <TargetFramework>net9.0</TargetFramework>
  <Nullable>enable</Nullable>
  <ImplicitUsings>enable</ImplicitUsings>
</PropertyGroup>
```

Central package management:

```xml
<!-- Directory.Packages.props -->
<Project>
  <PropertyGroup>
    <ManagePackageVersionsCentrally>true</ManagePackageVersionsCentrally>
  </PropertyGroup>
  <ItemGroup>
    <PackageVersion Include="Microsoft.EntityFrameworkCore" Version="9.0.0" />
    <PackageVersion Include="Microsoft.AspNetCore.OpenApi" Version="9.0.0" />
  </ItemGroup>
</Project>
```

Bump all related `Microsoft.*` packages in one commit to avoid mismatched shared framework references.

## CI Alignment

```yaml
# GitHub Actions example
- uses: actions/setup-dotnet@v4
  with:
    dotnet-version: '9.0.x'
- run: dotnet restore
- run: dotnet build --no-restore
- run: dotnet test --no-build
```

Docker base image must match major runtime:

```dockerfile
FROM mcr.microsoft.com/dotnet/aspnet:9.0 AS base
FROM mcr.microsoft.com/dotnet/sdk:9.0 AS build
```

## Incremental Migration for Multi-Target

When jumping several majors, prefer one major at a time (`net6` → `net8` → `net9`) if the codebase is large or heavily customized. Each step should produce a green build and test run.

## Verification Checklist

- `dotnet publish` succeeds with same RID if self-contained or native AOT
- No deprecated API warnings left unaddressed in hot paths
- Integration tests pass against updated test containers
- Staging deploy uses new runtime before production rollout
