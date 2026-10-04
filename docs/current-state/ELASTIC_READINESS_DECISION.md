# Elastic Readiness Decision

## Decision — Keep Elastic as conversion-only

The Mayuri lab was decommissioned in October 2026, so there is currently no live Splunk or Elastic backend owned by this repository.

### What remains valid

- canonical Sigma content remains in the repository
- generated Splunk and Elastic output remains useful for portability
- offline fixture testing and CI validation remain reusable
- historical Mayuri live-validation records retain their provenance

### Current boundary

Elastic should be described as **conversion supported, not live deployed or validated**.

The repository should also avoid describing Splunk as a current live backend. Existing Splunk validation is historical evidence from the retired Mayuri environment.

## Recommendation

- keep Elastic conversion visible as a portability feature
- keep current testing offline and repository-driven
- validate against future live SIEM backends only when an approved environment exists
- do not rebuild infrastructure solely to preserve an old platform claim
