---
name: angular-accessibility
description: Implement and review accessible Angular UIs with semantic templates, CDK a11y patterns, keyboard support, ARIA, and focus management. Use when building forms, dialogs, menus, tables, or fixing accessibility audit issues in Angular apps.
---

# Angular Accessibility

## Workflow

1. Prefer native HTML elements and Angular Material/CDK accessible primitives when project includes them.
2. Ensure labels, errors, and groups work with screen readers — associate `formControlName` fields with `<label>`.
3. Manage focus for dialogs, drawers, and route changes using CDK FocusTrap or component APIs.
4. Verify keyboard: Tab order, Enter/Space activation, Escape closes overlays, arrow keys in menus.
5. Check color contrast and visible focus indicators — do not remove outlines without replacement.
6. Use live announcer for async status when appropriate (`LiveAnnouncer` from CDK).
7. Test with keyboard-only navigation and spot-check VoiceOver/NVDA on critical flows.

## References

- Read `references/forms-and-semantics.md` for labels, errors, landmarks, and heading structure.
- Read `references/overlays-and-cdk.md` for dialogs, focus trap, and LiveAnnouncer.

## Checklist

- Buttons are `<button type="button|submit">` — not clickable divs.
- Icon-only controls have accessible names.
- Modal dialogs trap focus and restore on close.
- Dynamic errors use `role="alert"` or live region appropriately.
- Tables use proper headers for data grids.
- Route changes move focus to main heading or skip target when UX requires it.

## Output

Summarize a11y issues, fixes, components touched, and manual verification steps.
