# Eval: Angular Accessibility

## Prompt

Review a custom dropdown built with div clicks only. Make it keyboard accessible using project patterns (Material/CDK or native select).

## Expected Agent Behavior

- Adds roles/keyboard support or replaces with accessible component
- Documents Arrow/Enter/Escape/Tab behavior
- Associates labels and focus management
- Mentions manual screen reader check

## Failure Signals

- tabindex-only fix without listbox semantics
- Ignores focus return on close
- aria-label without keyboard operability
