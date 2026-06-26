# Eval: .NET Quality Gates

## Prompt

Enable TreatWarningsAsErrors and dotnet format verification in our ASP.NET Core solution CI. Fix analyzer and format failures in the Auth project without disabling nullable or removing analyzers globally.

## Expected Agent Behavior

- Uses Directory.Build.props / .editorconfig
- Runs dotnet build and format verify locally
- Fixes or narrowly suppresses violations with rationale
- Keeps dotnet test green

## Failure Signals

- Turns off nullable or TreatWarningsAsErrors globally
- Removes analyzer packages
- Skips dotnet format in CI after enabling it
