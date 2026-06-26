# .NET Analyzers, Format, and Coverage

## Directory.Build.props Pattern

```xml
<Project>
  <PropertyGroup>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
    <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
    <AnalysisLevel>latest</AnalysisLevel>
    <EnforceCodeStyleInBuild>true</EnforceCodeStyleInBuild>
  </PropertyGroup>
</Project>
```

Introduce `TreatWarningsAsErrors` incrementally on legacy solutions — use `WarningsNotAsErrors` for known debt with ticket links.

## .editorconfig

- Centralize indent, naming, and analyzer severity overrides.
- Do not duplicate StyleCop rules in both `.editorconfig` and `stylecop.json` without reason.

## Roslyn / StyleCop Analyzers

```xml
<ItemGroup>
  <PackageReference Include="StyleCop.Analyzers" Version="1.2.0-beta.556">
    <PrivateAssets>all</PrivateAssets>
  </PackageReference>
</ItemGroup>
```

Fix violations in touched files; use `GlobalSuppressions.cs` sparingly with justification.

## dotnet format

```bash
dotnet format
dotnet format --verify-no-changes   # CI
dotnet format --severity warn
```

Wire format check into CI when the team adopts it — do not rely on IDE-only formatting.

## Coverlet Coverage

```xml
<PackageReference Include="coverlet.collector" Version="6.0.4" />
```

Parse coverage in CI (ReportGenerator, Sonar) and enforce minimum on critical projects — not solution-wide vanity metrics.

Exclude:

- Generated code
- Program entry boilerplate

Do not exclude domain/services to pass a threshold.

## Nullable Reference Types

- Enable `<Nullable>enable</Nullable>` for new projects.
- Fix nullability in changed APIs — avoid `!` suppression without guard.
- Use `#nullable disable` only at legacy file boundaries with migration plan.

## Common Failure Fixes

| Failure | Approach |
| --- | --- |
| CA1031 catch Exception | Catch specific types or rethrow with context |
| SA1600 missing docs | Add docs on public API or adjust rule for internal-only projects |
| Test fail on CI only | Check culture, timezone, path separators |
| Format verify fail | Run `dotnet format` locally and commit |

## Related Skills

- `dotnet-testing-verification` — test quality behind gates
- `dotnet-aspnet-service` — API code under analysis
