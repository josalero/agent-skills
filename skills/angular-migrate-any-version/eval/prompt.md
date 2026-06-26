# Eval: Angular Migrate Any Version

## Prompt

Plan upgrade from Angular 15 (NgModules, *ngIf/*ngFor) to Angular 19 standalone + control flow. App has 60 feature modules and Karma tests.

## Expected Agent Behavior

- Recommends sequential ng update majors or justified jumps with guide links
- Phases module→standalone migration separately from version bump
- Addresses TestBed and router guard migration
- Includes CI Node/TS alignment and verification gates

## Failure Signals

- Single PR converting all modules and version jump
- Ignores third-party library compatibility
- No test/build verification steps
