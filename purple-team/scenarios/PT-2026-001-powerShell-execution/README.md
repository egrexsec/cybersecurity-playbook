# PT-2026-001 — PowerShell Execution

This scenario is the first end-to-end Mayuri purple-team validation workflow.
It stays narrowly scoped to the approved Windows victim and validates:

- preflight safety checks
- baseline telemetry capture
- approved PowerShell execution simulation
- targeted evidence collection
- hunt development
- forensic reconstruction
- Sigma authoring
- Wazuh test-scope validation
- positive / variant / negative validation loops

The scenario is intentionally **public-repo friendly**:
- no credentials
- no raw evidence dumps
- no large binaries
- no unsafe or destructive payloads
- no uncontrolled internet callbacks
