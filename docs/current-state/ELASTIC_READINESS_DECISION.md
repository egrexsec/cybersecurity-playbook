# Elastic Readiness Decision

## Decision A — Defer Elastic

## Evidence for deferral
Elastic conversion is implemented, but the repository should still be presented as a **Splunk-first, lab-validated detection-engineering repository**.

### What is complete
- three live-validated scenarios on main
- three canonical Sigma rules on main
- generated Splunk and Elastic query output on main
- offline fixture testing on main
- GitHub Actions workflow for offline validation and secret scanning

### Why Elastic is still deferred
1. **No live Elastic backend is deployed or validated**
2. **Splunk field normalization is still incomplete**, so even the primary backend retains lab-specific translation caveats
3. **Offline EVTX workflow is documented but not fully operationalized**
4. **Current portfolio value is stronger from honest Splunk-first validation than from claiming cross-SIEM parity without live evidence**

## Recommendation
- keep Elastic conversion visible as a portability feature
- describe it as **conversion supported, not live deployed**
- revisit live Elastic only after broader scenario coverage, stronger field normalization, and more mature DFIR workflows
