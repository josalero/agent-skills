---
name: php-migrate-any-version
description: Plan and execute PHP version migrations. Use when upgrading PHP runtime, Composer platform requirements, framework versions, extensions, CI images, Docker bases, deprecated APIs, static analysis rules, or test strategy across PHP versions.
---

# PHP Migrate Any Version

## Workflow

1. Detect current PHP runtime, target version, Composer platform config, framework version, extensions, CI image, and Docker base image.
2. Identify whether the upgrade includes Laravel, Symfony, or extension changes.
3. Read the relevant migration path reference before changing code.
4. Upgrade build and platform configuration first, then dependencies, then source incompatibilities.
5. Run tests and static analysis after each meaningful migration step.
6. Verify runtime behavior, container images, CI, and deployment configuration.

## References

- Read `references/version-paths.md` for common PHP version migration paths and breaking changes.
- Read `references/toolchain-and-ci.md` for Composer, PHPStan, CI, Docker, and verification commands.

## Output

After each migration step, summarize:

- Current and target PHP, framework, and extension versions
- Configuration files changed
- Source or dependency fixes applied
- Tests and analysis run with results
- Remaining blockers, deprecated API usage, or CI/container updates needed
