# Roadmap

## Current foundation

### Completed
- PT-2026-001 validated end-to-end against live lab telemetry
- PT-2026-002 validated end-to-end against live lab telemetry
- PT-2026-003 validated end-to-end against live lab telemetry
- Sigma linting, conversion, and fixture testing implemented
- Splunk live validation workflow implemented
- public-safe validation evidence and investigation documentation published

## Next detection coverage

### Phase 1 — Windows persistence / execution expansion
- **T1053.005 Scheduled Task/Job**
  - Acceptance: scenario, Sigma rule, fixtures, and live validation record committed
- **T1543.003 Windows Service**
  - Acceptance: scenario, Sigma rule, fixtures, and live validation record committed
- **Account or group modification**
  - Acceptance: one low-risk scenario with positive/negative tests and sanitized evidence
- **Safe credential-access simulation**
  - Acceptance: one bounded scenario demonstrating telemetry + detection without unsafe secrets handling
- **Network or DNS behavior**
  - Acceptance: one scenario tying host behavior to network-oriented detection content
- **One multi-stage attack chain**
  - Acceptance: at least two linked techniques with cross-artifact validation evidence

### Phase 2 — Detection platform maturity
- **Field normalization improvements**
  - Acceptance: documented reduction in raw-XML-only matching for live Splunk queries
- **Durable Splunk saved searches / alerts**
  - Acceptance: saved search objects defined, documented, and verified in the lab
- **Standardized validation latency**
  - Acceptance: live validation records contain computed ingestion/detection latency fields
- **Detection quality scoring**
  - Acceptance: rules carry a consistent quality rubric or scorecard
- **ATT&CK coverage reporting**
  - Acceptance: repo-derived coverage report generated from current scenarios and rules
- **Rule versioning and regression tests**
  - Acceptance: changes to validated rules can be compared and regression-tested automatically

### Phase 3 — DFIR expansion
- **Velociraptor collections**
  - Acceptance: repeatable collection workflows linked to at least one validated scenario
- **Windows event-log triage**
  - Acceptance: documented analysis path from raw Windows events to detection evidence
- **Timeline generation**
  - Acceptance: at least one case study includes structured timeline output
- **Disk artifact review**
  - Acceptance: one scenario includes file-system artifact handling beyond process/event evidence
- **Memory-forensics workflow**
  - Acceptance: documented, safe, and reproducible memory workflow for future scenarios

### Phase 4 — Cloud expansion
- **AWS investigation content**
  - Acceptance: one validated cloud-oriented case study or detection workflow
- **Azure investigation content**
  - Acceptance: one structured Azure-focused detection or hunt artifact set
- **GCP investigation content**
  - Acceptance: one structured GCP-focused detection or hunt artifact set
- **Cloud detection validation**
  - Acceptance: at least one cloud detection includes fixture or replay-based validation

## Portfolio acceptance goals
- a visitor can understand the repo structure and current state quickly
- a detection engineer can trace scenario -> rule -> query -> fixture -> live evidence
- generated vs canonical content remains clearly separated
- public-safe posture remains intact
