# AI-assisted investigations

## Policy

AI output is not evidence. It is untrusted analytical assistance and must not be cited as the factual basis for a finding, timeline event, indicator, attribution, or response decision.

## Appropriate uses

- propose search terms, pivots, or competing hypotheses
- explain a tool or log field for analyst review
- draft queries that are tested against known data
- summarize sanitized notes while preserving source references
- identify documentation gaps or inconsistent reasoning

## Prohibited or unsafe uses

- uploading raw evidence, credentials, tokens, personal data, or sensitive infrastructure details to an unapproved service
- treating generated facts, citations, decoded content, or timelines as verified
- allowing AI to modify originals or the private evidence ledger
- using generated conclusions without reproducing them from source artifacts
- concealing uncertainty or tool errors behind polished prose

## Validation requirements

1. Provide only data approved for the selected tool and handling boundary.
2. Record the model or tool, task, sanitized inputs, and date when its contribution materially affects analysis.
3. Treat every generated query, transformation, timestamp, and assertion as untrusted.
4. Reproduce outputs with deterministic tools or direct source review.
5. Cite evidence identifiers and analyst-verified results, never the AI response, in conclusions.
6. Document where AI assistance was rejected or could not be validated.

The analyst remains accountable for scope, evidence handling, reasoning, and conclusions.
