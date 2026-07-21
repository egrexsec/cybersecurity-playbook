# Elastic readiness decision

## Decision — defer live Elastic

Elastic query generation is implemented, but the repository must describe that target as **conversion supported, not live deployed**.

## Current repository evidence

- 11 canonical Sigma rules.
- 59 passing positive and negative fixtures.
- Generated Splunk SPL and Elastic EQL.
- 11 sanitized historical validation summaries from an earlier Splunk-centered lab cycle.
- GitHub Actions for offline validation, unit tests, public-safety checks, and secret scanning.

## Why live Elastic remains deferred

1. No live Elastic backend is deployed or validated by current repository evidence.
2. Historical Splunk validation used environment-specific raw XML matching where normalized fields were unavailable.
3. Generated query syntax does not prove index, table, parser, mapping, or data-model compatibility.
4. The offline EVTX workflow is documented but not fully operationalized.

## Recommendation

- Keep Elastic EQL visible as a portability artifact.
- Preserve canonical Sigma as the authored source.
- Do not claim cross-SIEM parity from conversion alone.
- Revisit live Elastic only after a separately authorized deployment and fixture-to-backend validation cycle.
