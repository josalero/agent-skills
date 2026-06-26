---
name: angular-testing-verification
description: Write and review Angular tests with TestBed, Jasmine/Jest, HttpClientTestingModule, and Testing Library patterns. Use when adding component tests, testing services and pipes, mocking HTTP, or improving Angular CI verification.
---

# Angular Testing Verification

## Workflow

1. Inspect test runner (Karma/Jest), Angular testing utilities, and existing spec conventions.
2. Test behavior visible to users — DOM text, roles, enabled/disabled — not private fields.
3. Configure TestBed with standalone imports or NgModule matching production.
4. Mock HTTP with `HttpClientTestingModule` and expectOne/verify.
5. Use `fakeAsync`/`tick` for debounce/timer logic; `waitForAsync` when appropriate.
6. Provide harnesses or TestBed helpers to reduce boilerplate in large apps.
7. Run focused tests: `ng test --include='**/order*.spec.ts'` or project equivalent.

## References

- Read `references/testbed-and-components.md` for component setup, queries, and async fixture.
- Read `references/http-and-services.md` for HttpClientTestingModule and service tests.

## Checklist

- Tests are isolated — order independent.
- HTTP mocked at HttpClient layer, not arbitrary service spies unless unit-testing logic.
- Router testing uses `RouterTestingModule` or provideRouter with stubs.
- Error and loading branches covered for data components.
- No tests that only assert component truthy without behavior.
- CI command documented and matches local script.

## Output

Summarize behaviors tested, TestBed setup choices, mocks used, and commands to run.
