# Timeline analysis

## Goal

Build a source-cited sequence of activity that separates observed events from analyst inference and makes clock, collection, and retention limits visible.

## Normalization rules

- retain the original timestamp, timezone, and source field
- add a normalized UTC timestamp for correlation
- record known clock drift and do not silently correct uncertain values
- preserve event identifiers, evidence IDs, and source paths needed to reproduce each row
- label inferred ordering, estimated times, and duplicate events explicitly
- distinguish event time, ingestion time, modification time, and acquisition time

## Recommended timeline fields

| Field | Description |
|---|---|
| Normalized time | UTC correlation value |
| Original time | Source value with timezone or offset |
| Evidence ID | Link to the private evidence ledger |
| Source | Log, artifact, sensor, or acquisition |
| Host / identity | Relevant system or principal |
| Activity | Neutral description of the observation |
| Interpretation | Analyst assessment, kept separate from the observation |
| Confidence | High, medium, or low with rationale |
| Related hypothesis | Question supported or challenged by the row |

## Analysis method

1. Seed the timeline with the alert or known event.
2. Expand backward to likely initial access or setup activity.
3. Expand forward through execution, persistence, discovery, movement, impact, and response.
4. Correlate across sources using time plus independent attributes such as process ID, logon ID, task name, service name, account, address, or file hash.
5. Mark gaps rather than filling them with assumptions.
6. Revisit hypotheses after each material pivot.
7. Publish a sanitized timeline that still points to stable evidence identifiers.
