# Eval: API Design Review

## Prompt

Review this proposed endpoint change for backward compatibility and contract quality. Recommend fixes.

```http
PATCH /api/v1/users/{id}
```

Before: accepts `{ "displayName": "..." }`, returns `200` with full user including `email`.

After: accepts `{ "name": "..." }` (renamed field), returns `204` on success, removes `email` from response, returns `400` with plain text body on validation error.

## Expected Agent Behavior

- Flags breaking renames, status code change, response shape change, and inconsistent error format
- Recommends additive migration (support both fields, deprecate old) or explicit `/v2`
- Proposes Problem Details for errors and documents client impact
- Suggests contract tests and deprecation headers if phasing change

## Failure Signals

- Approves breaking changes without version or migration plan
- Only nitpicks naming without compatibility analysis
- Ignores security implication of removing/ exposing email
