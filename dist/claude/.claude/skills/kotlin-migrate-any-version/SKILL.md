---
name: kotlin-migrate-any-version
description: Plan and execute Kotlin version migrations for Gradle and Maven projects. Use when upgrading Kotlin compiler, language version, JVM target, K2 compiler, kotlinx libraries, or fixing deprecation and binary compatibility breaks after a Kotlin bump.
---

# Kotlin Migrate Any Version

## Workflow

1. Record current Kotlin version, JVM target, compiler options, and dependent kotlinx library versions from build files.
2. Read release notes and compatibility matrix for the target Kotlin version.
3. Produce a phased plan: toolchain bump, dependency alignment, compile fixes, test verification, CI update.
4. Upgrade in a dedicated branch; fix compiler errors before runtime surprises.
5. Run full test suite and spot-check critical modules for behavior changes (coroutines, serialization, reflection).
6. Update CI images and developer docs (`jenv`, `.java-version`, Gradle toolchain).

## References

- Read `references/migration-planning.md` for phased rollout, risk assessment, and rollback strategy.
- Read `references/build-and-compatibility.md` for Gradle/Maven configuration, JVM target alignment, and library version pins.

## Migration Checklist

- Kotlin, JVM target, and Spring/Ktor versions are compatible.
- kotlinx.coroutines, serialization, and metadata libraries aligned with compiler.
- `-X` compiler flags and opt-ins reviewed for deprecated options.
- All modules compile before merging.
- CI uses the same JDK and Kotlin versions as local builds.
- Rollback path documented if production issues appear.

## Output

Summarize current and target versions, phased plan, files changed, verification commands, known risks, and rollback steps.
