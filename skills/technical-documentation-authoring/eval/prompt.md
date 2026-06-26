# Eval: Technical Documentation Authoring

## Prompt

Draft a short RFC for moving our monolith's reporting module to an async export job (background worker + signed download URL). Include motivation, detailed design outline, alternatives, rollout, testing, and open questions. Use proper RFC structure and tables where helpful.

Do not write production code.

## Expected Agent Behavior

- Uses RFC template sections (summary, motivation, design, alternatives, rollout, testing, drawbacks, questions)
- Scannable formatting: headings, tables, short paragraphs
- Testable acceptance or verification criteria in testing section
- Labels assumptions clearly
- Cross-references design analysis concepts (options, tradeoffs) without inventing fake metrics

## Failure Signals

- Unstructured essay with no headings
- Missing alternatives or rollout plan
- Jumps to class-level implementation as main content
- Vague "we will ensure quality" without verification steps
- Wall of text without tables or lists
