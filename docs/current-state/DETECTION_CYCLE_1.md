# Detection Cycle 1 — CTI-Informed Web Delivery and Proxy Execution

## Bounded scope

Cycle 1 converts current OpenCTI evidence of malicious web-delivered HTA and executable content into two behavior-focused Windows detection gaps: PowerShell web retrieval to file (T1105) and `mshta` child-process execution (T1218.005). It does not import active IOC strings into public detection logic.

## Hypothesis

A web-delivery chain that retrieves staged content with a trusted native utility and then proxies execution through `mshta` should be observable as independent process behaviors and as a temporally correlated chain.

## Safety contract

- One approved Windows victim only.
- Exact pinned Atomic UUIDs; no sibling-test bulk execution.
- Loopback-only HTTP, benign text/HTA content, and no external C2.
- No credential access, lateral movement, persistence, or destructive actions.
- Private rollback reference, bounded execution, verified cleanup, and a second cleanup pass.
- Public evidence uses role labels and excludes environment identifiers and raw active IOCs.

## CTI basis

The operational CTI platform contained current URL-delivery indicators including HTA, executable, and script-like content, while ATT&CK enrichment supplied T1105 and T1218.005 semantics. Public artifacts retain only source classes, counts, retrieval date, and behavioral conclusions.

## Deliverables

- PT-2026-014: PowerShell web ingress transfer.
- PT-2026-015: mshta-to-shell or script-interpreter execution.
- HUNT-2026-014 through HUNT-2026-016.
- CAMPAIGN-2026-001: benign transfer-to-execution chain.
- Exact and modified positives, three negatives per rule, live telemetry, offline fixtures, cleanup, and independent review.

## Completed results

- OpenCTI semantic sample: 500 indicators reviewed; 433 current seven-day indicators; 423 URL-pattern indicators; 129 script-like URLs; 16 HTA-like URLs; both ATT&CK techniques resolved semantically.
- HUNT-2026-014 through HUNT-2026-016: 30-day uncontrolled baselines returned zero matches; controlled validation and campaign windows produced expected evidence.
- PT-2026-014: exact and modified positives detected; three controls quiet; cleanup idempotent.
- PT-2026-015: exact inline Atomic prevented by endpoint protection before child creation; modified and campaign child-process behaviors detected; three controls quiet; cleanup idempotent.
- CAMPAIGN-2026-001: loopback-only transfer, mshta execution, and benign PowerShell child completed; T1105 and T1218.005 detections correlated three seconds apart.

### Safety deviation

A candidate remote-HTA Atomic was rejected when its SYSTEM/noninteractive controller path did not honor the intended safe input override. Its default payload attempted an outbound external connection, and the connection failed. Execution was stopped, no connection was established, all temporary processes/files were removed, no sensor impact remained, and that UUID was excluded from the selected scenario.
