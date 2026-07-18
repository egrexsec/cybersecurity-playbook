# Attack Plan

## Scenario hypothesis
If a low-risk PowerShell decode-and-execute pattern is replayed on the approved Windows victim, the lab should produce enough process and PowerShell telemetry to build and validate a behavioral detection.

## Expected behavior
- encoded content is decoded and invoked through PowerShell
- marker artifacts are created under controlled paths
- PowerShell operational logging records the script content

## Safety controls
- approved victim only
- low-risk commands only
- explicit cleanup after execution
- no secrets or external payload staging required

## Rollback considerations
- snapshot prerequisite is required in the scenario definition
- cleanup removes created markers and temporary registry artifacts

## Test reference
Source of truth:
- `purple-team/scenarios/PT-2026-001-powerShell-execution/scenario.yaml`
- `automation/execution/pt_2026_001_atomic_positive.ps1`
- `automation/execution/pt_2026_001_variant.ps1`
