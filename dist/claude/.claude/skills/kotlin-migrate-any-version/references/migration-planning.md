# Kotlin Migration Planning

## Phase 1 — Inventory

- Kotlin plugin version in root `build.gradle.kts`
- `jvmToolchain` or `jvmTarget`
- kotlinx library BOM or explicit versions
- Compiler opt-ins and `-X` flags

## Phase 2 — Upgrade Order

1. Bump Kotlin Gradle plugin in a branch
2. Align kotlinx dependencies
3. Fix compile errors module by module
4. Run tests per module, then full suite
5. Update CI JDK/Kotlin matrix

## Risk Areas

- K2 compiler behavior differences
- Inline/reified API changes
- Serialization format compatibility
- Spring Boot Kotlin support minimums

## Rollback

Keep the previous Kotlin version tag and document the revert commit range.
