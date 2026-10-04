# Detection Cycle 1 Coverage Matrix

| Priority | Technique | Behavior | CTI relevance | Scenario / campaign stage | Detection | Fixtures | Hunt | Live evidence | Cleanup / limitation |
|---|---|---|---|---|---|---|---|---|---|
| High | T1105 | PowerShell retrieves web content to file | Current malicious URL and script-delivery classes | PT-2026-014; campaign stage 1 | DET-2026-014; authored Sigma plus generated Splunk/Elastic | 2 positive / 3 negative | HUNT-2026-014, HUNT-2026-016 | Exact and modified positives detected; campaign corroborated | Clean twice; depends on PowerShell script-block telemetry |
| High | T1218.005 | Mshta launches a shell or script child | Current HTA delivery class | PT-2026-015; campaign stages 2–3 | DET-2026-015; authored Sigma plus generated Splunk/Elastic | 2 positive / 3 negative | HUNT-2026-015, HUNT-2026-016 | Exact inline Atomic prevented; modified and campaign lineage detected | Clean twice; Defender prevention and child-process detection are separate controls |
| Existing dependency | T1059.001 | PowerShell child execution | Common execution layer | Campaign stage 3 | Existing validated PowerShell coverage | Existing fixtures | HUNT-2026-016 | Benign campaign marker and script telemetry verified | Reused, not represented as a new scenario |
| Medium | T1027 | Obfuscated content | Enriched ATT&CK context | None in Cycle 1 | Existing PowerShell coverage only | Existing | Future cycle | Not replayed | Hunt and defer new Atomic until a bounded hypothesis exists |
| Deferred | Credential access and lateral movement | Higher-impact behaviors | Potentially relevant | Excluded | None added | None added | Future separately authorized cycle | Not executed | Requires separate authorization and stronger rollback gates |

Queue depth was not used as semantic CTI proof. Selection required platform-visible ATT&CK/CAPEC content, current indicator classes, available telemetry, safe reproducibility, and a concrete residual gap.
