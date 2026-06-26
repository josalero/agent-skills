# Eval: AI Evaluation Architecture

## Prompt

Our RAG support bot went to production last month. We have no golden dataset. Product wants a "quality score" before we switch embedding models next week. The team has JUnit tests for the API but nothing for answer correctness. Design an evaluation architecture we can implement in two sprints.

## Expected Agent Behavior

- Defines task success and splits retrieval vs generation vs safety eval
- Proposes golden dataset structure (20–50 cases) with categories including unanswerable and ACL
- Recommends offline gates before embedding swap with recall@k and citation checks
- Warns against LLM-as-judge-only; includes human review sample
- Suggests minimal harness (JSON cases + CI script) and versioning trigger for embed change
- Does not conflate unit tests with semantic answer eval

## Failure Signals

- "Just add more JUnit tests" without retrieval/answer metrics
- No baseline before model/index change
- Single subjective score with no rubric or categories
- Ignores production drift monitoring
- No phased plan (two-sprint scope ignored)
