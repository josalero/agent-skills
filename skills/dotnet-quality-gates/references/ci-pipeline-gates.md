# .NET CI Pipeline Gates

## Canonical Commands

```bash
dotnet restore
dotnet build --configuration Release --no-restore
dotnet test --configuration Release --no-build --verbosity normal
dotnet format --verify-no-changes
```

Combine into one CI step or separate jobs by duration.

## Example GitHub Actions

```yaml
jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-dotnet@v4
        with:
          global-json-file: global.json
      - run: dotnet restore
      - run: dotnet build -c Release --no-restore
      - run: dotnet test -c Release --no-build --collect:"XPlat Code Coverage"
      - run: dotnet format --verify-no-changes
```

## PR vs Main

| Stage | PR | Main |
| --- | --- | --- |
| Build + analyzers | Yes | Yes |
| Unit tests | Yes | Yes |
| Integration tests | Subset or nightly | Full |
| Format verify | Yes | Yes |
| Coverage upload | Optional | Recommended |

## Blocking vs Advisory

Block merge on: test failures, build errors, format drift (when enforced), new analyzer errors in changed projects.

Use advisory Sonar or legacy warnings only with explicit team waiver.

## Local Parity

```bash
dotnet --version    # match global.json
dotnet build -c Release
dotnet test -c Release
```

Document required SDK in README.

## Related Skills

- `dotnet-cloud-native-delivery` — container build after gates pass
- `testing-strategy` — integration test placement
