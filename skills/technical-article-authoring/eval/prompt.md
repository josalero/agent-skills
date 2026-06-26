# Eval: Technical Article Authoring

## Prompt

Draft a LinkedIn long-form article explaining why agentic workflows (supervisor + specialized sub-agents) beat a single monolithic prompt for a WhatsApp-driven content pipeline. Audience: senior backend engineers evaluating LangChain-style orchestration. Include a hook, outline, full draft with at least three sections, takeaways, and a comment-driving CTA. No production code — one short pseudo-diagram or mermaid flow is enough.

## Expected Agent Behavior

- Identifies article type (opinion/deep-dive hybrid) and audience upfront
- Uses scannable structure: hook, headings, short paragraphs
- Provides concrete orchestration tradeoffs (latency, debuggability, prompt drift)
- Includes takeaways and platform-appropriate CTA
- Applies pre-publish checklist or calls out deferred items
- Does not produce RFC/BRD template by mistake

## Failure Signals

- Opens with "In this article I will explain..."
- Wall of text without headings
- Generic AI buzzwords without tradeoffs
- Full Java class implementations as main content
- Missing hook or CTA
- Copies internal BRD/RFC section numbering
