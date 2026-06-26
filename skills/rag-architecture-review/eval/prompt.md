# Eval: RAG Architecture Review

## Prompt

Review a product catalog chatbot: embeddings in pgvector, chunks are 2000 characters fixed-size, no metadata filters, top-k=20 passed to GPT. Users sometimes get wrong product recommendations and answers about other stores' products. Recommend architecture fixes.

## Expected Agent Behavior

- Identifies missing tenant/product metadata filters and ACL at retrieval
- Questions fixed 2000-char chunking for structured product data
- Recommends hybrid search for SKUs, reranking, lower effective k with citations
- Proposes golden eval set and reindex plan
- Mentions prompt injection from catalog text and audit logging

## Failure Signals

- Suggests only "better prompt" without retrieval fixes
- Ignores cross-store leakage
- Recommends larger k only
- No eval or operational guidance
