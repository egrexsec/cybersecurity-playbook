# Elastic Readiness Decision

## Decision A — Defer Elastic

## Evidence for deferral
The minimum milestone is **not fully met for safe platform expansion**, even though three scenarios and three Sigma rules are now live-validated in Splunk.

### What is complete
- Three prior scenarios are verified: PT-2026-001, PT-2026-002, PT-2026-003
- Three Sigma rules exist and pass local fixture testing
- Splunk conversion succeeds for all three rules
- Elastic conversion succeeds syntactically for all three rules
- All three rules have positive fixtures and at least three negative fixtures
- All three rules were replayed live against Splunk on 2026-07-18
- At least two modified variants were detected live (in fact, all three were)

### Why Elastic is still deferred
1. **Splunk field normalization is incomplete**
   - Live detections currently rely on raw XML `_raw` matching rather than a normalized field/CIM model.
2. **Offline EVTX capability is not yet operational**
   - Workflow is documented, but Chainsaw/Hayabusa are not yet integrated.
3. **GitHub CI is not yet in place on this branch**
   - There is no enforced PR gate for Sigma, fixtures, secrets, and validation-record completeness yet.
4. **Capacity risk**
   - Host root filesystem is ~80% used with ~19G free.
   - Host memory currently shows low free headroom.
   - SOC01 already carries Wazuh + Splunk duties; another SIEM on SOC01 would be destabilizing.

## Required next steps before Elastic
1. Finish Splunk XML field normalization / mapping cleanup.
2. Add GitHub Actions for Sigma, fixtures, secret scanning, and validation-record gates.
3. Operationalize offline EVTX export + Chainsaw/Hayabusa analysis.
4. Confirm storage/memory placement for an Elastic stack **outside** the already-loaded SOC01 role.

## Current recommendation
- Keep Splunk as the primary live validation backend.
- Treat Elastic conversion as portability-only for now.
- Revisit deployment only after the above gaps are closed.
