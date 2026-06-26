# Eval: Cloud Native Delivery

## Prompt

Our org has 12 microservices with 4 different CI pipelines (GitHub Actions, Jenkins, manual scripts). Deploys to production are weekly batch windows; rollbacks are rare and manual. Propose a cross-stack delivery standard and a 90-day roadmap without mandating single cloud or language.

## Expected Agent Behavior

- Assesses inconsistency risk and recommends golden pipeline template
- Defines environment promotion, immutable tags, and smoke verification
- Proposes phased rollout (pilot team, then expand) not big-bang mandate
- Covers secrets, scanning, rollback, and platform checklist at high level
- References ecosystem skills for Java/Node specifics where relevant

## Failure Signals

- Mandates Kubernetes for everything immediately
- Ignores rollback and staging parity
- No phased adoption plan
- Only tool list without standards and verification
