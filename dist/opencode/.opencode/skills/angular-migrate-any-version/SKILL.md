---
name: angular-migrate-any-version
description: Plan and execute Angular version and toolchain migrations including standalone APIs, routing, testing, and breaking changes across major releases. Use when upgrading Angular, migrating from NgModules to standalone, or updating RxJS and TypeScript peers.
---

# Angular Migrate Any Version

## Workflow

1. Inventory: Angular core/cli version, Node, TypeScript, RxJS, testing stack, and third-party UI libraries.
2. Read official Angular update guide for target version sequence — upgrade one major at a time when jumping multiple versions.
3. Run `ng update @angular/core @angular/cli` and aligned packages; resolve peer dependency warnings explicitly.
4. Apply schematic migrations when offered; fix compile errors incrementally.
5. Update breaking APIs: standalone bootstrap, functional guards, control flow syntax, inject() patterns.
6. Run unit tests and smoke critical routes after each major step.
7. Document deferred cleanups (NgModule removal, legacy APIs) in follow-up tickets.

## References

- Read `references/upgrade-sequencing.md` for ng update order and incremental strategy.
- Read `references/breaking-changes-checklist.md` for standalone, control flow, and router updates.

## Checklist

- `@angular/core` and `@angular/cli` versions aligned.
- TypeScript within supported range for target Angular.
- Third-party libraries verified compatible or upgraded.
- `angular.json` and builders updated if required.
- CI uses same Node/npm versions as local upgrade doc.
- Rollback plan: branch + lockfile tag before migration PR merge.

## Output

Summarize version path, commands run, breaking fixes, verification, and remaining manual migrations.
