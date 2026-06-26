# Eval: Migration Planning

## Prompt

We need to migrate a Rails monolith's reporting module to a new Java service over 6 months without a big-bang rewrite. Reporting is read-heavy, uses the shared PostgreSQL database today, and serves an internal admin UI plus a nightly CSV export job. Propose a phased migration plan with risks and verification.

## Expected Agent Behavior

- Recommends strangler or phased read migration before writes
- Addresses shared DB coupling and eventual data ownership split
- Sequences phases with deployable increments and decommission criteria
- Includes parity checks for CSV export and admin UI
- Outputs risk register and comms needs

## Failure Signals

- Big-bang rewrite in one phase
- Ignores shared database problem
- No verification or rollback/forward-fix discussion
- Missing consumer inventory (admin UI, batch job)
