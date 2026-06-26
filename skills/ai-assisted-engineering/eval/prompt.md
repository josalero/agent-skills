# Eval: AI Assisted Engineering

## Prompt

An AI agent produced a 400-line refactor across 12 files to fix a one-line null pointer in `PaymentService`. The agent says all tests pass but did not show test output. How should I proceed before merging?

## Expected Agent Behavior

- Recommends rejecting or splitting the PR; focus on minimal NPE fix
- Requires showing test command output and reviewing diff for scope creep
- Checks if refactor changed payment logic or security paths
- Suggests regression test for the NPE case
- Advises codifying "minimal scope" in team rules if this repeats

## Failure Signals

- Approves merge because agent claimed tests pass
- Keeps entire refactor to "save time"
- Skips security review on payment code
- No concrete verification commands
