# Memory triage

**Capability maturity: Planned**

No memory acquisition or analysis case is claimed as verified in this repository. This workflow defines the evidence and safety bar for future implementation.

## Use cases

Memory triage may be appropriate for volatile process state, injected code, in-memory credentials, active connections, decrypted configuration, or artifacts unavailable on disk. Collection must be authorized because acquisition can affect system state and may capture highly sensitive material.

## Planned workflow

1. Record authorization, host state, uptime, time, and collection rationale.
2. Select a tested acquisition tool appropriate to the operating system and architecture.
3. Capture to encrypted private storage with sufficient capacity.
4. Hash and verify the image after acquisition and transfer.
5. Record tool version, command line, acquisition duration, errors, and image metadata.
6. Analyze a working copy with a documented framework and symbol or profile source.
7. Start with process, parent-child, command-line, module, handle, network, and suspicious-memory triage.
8. Validate plugin output against other plugins or non-memory sources before drawing conclusions.
9. Keep the image and sensitive extracts private; publish only sanitized observations.

## Readiness criteria

The capability can move from Planned to Installed when acquisition and analysis tooling is available with private storage controls. It becomes Verified only after a known test image is acquired or analyzed reproducibly. Live validated requires an approved live lab case with an evidence ledger, integrity checks, documented analysis, and sanitized results.
