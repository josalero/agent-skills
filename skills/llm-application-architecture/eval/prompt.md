# Eval: LLM Application Architecture

## Prompt

We want to add a "help me choose a health plan" chatbot to our benefits portal. HR policy PDFs update quarterly; eligibility and pricing live in our PostgreSQL member API. The product manager asked for "RAG on the PDFs and GPT-4." Team is two backend devs, one frontend dev. Target p95 latency under 8 seconds. Recommend an LLM application architecture before we start coding.

## Expected Agent Behavior

- Clarifies user job (recommendation vs enrollment action) and separates static policy text from live eligibility/pricing
- Recommends hybrid: RAG for policy PDFs + tools for member/eligibility API — not RAG-only or prompt-only
- Discusses sync chat with streaming vs async for heavy lookups; cites latency budget
- Mentions model routing/fallback and cost controls at high level
- Calls out ACL (member can only see own data) and eval plan before build
- Suggests phased MVP and follow-on skills (RAG review, tool design, eval architecture)
- Does not jump straight to fine-tuning or "bigger context window" as the main fix

## Failure Signals

- Accepts "RAG on PDFs only" for live pricing/eligibility
- No tool/API layer for transactional data
- No mention of authorization or tenant/member scoping
- No MVP phasing or eval mention
- Recommends fine-tuning as first step
