# PT-2026-012 Results

## Validation run
- Validation ID: `VAL-2026-012`
- Technique: `T1569.002` Service Execution
- Exact Atomic test: `2382dee2-a75f-49aa-9378-f52df6ed3fb1` (`T1569.002-1`)
- Status: **live validated** on 2026-07-29 UTC
- Target: approved Windows victim only
- Rollback snapshot: `pre-pt-2026-012-t1569-002-20260729`

## Scope and distinction
This scenario validates **execution through the Service Control Manager**: a started service causes `services.exe` to launch a command interpreter as `SYSTEM`. It complements but does not duplicate `PT-2026-005` (`T1543.003`), whose primary analytic focus is service creation telemetry.

No domain controller execution, remote service creation, lateral movement, credential access, destructive payload, or uncontrolled network activity was permitted.

## Positive paths
1. The exact upstream Atomic UUID ran with a controlled PowerShell marker command under service name `PT-2026-012-Original`.
   - Marker created successfully.
   - Splunk detected `services.exe -> cmd.exe -> powershell.exe` at `2026-07-29T16:55:23Z`.
   - SCM events `7045`, `7009`, and `7000` corroborated service installation and the expected non-service payload timeout.
   - The Atomic cleanup deleted the service.
2. The same exact UUID ran with a modified `cmd.exe /d /c echo` marker command under `PT-2026-012-Variant`.
   - Marker created successfully.
   - Splunk detected `services.exe -> cmd.exe` at `2026-07-29T16:58:32Z`.
   - SCM events `7045`, `7009`, and `7000` corroborated the behavior.
   - The Atomic cleanup deleted the service.

The SCM timeout is expected because the deliberately inert marker commands are not service-aware binaries. Command execution and detection occurred before SCM reported the timeout.

## Negative paths
The behavioral Sigma rule remained quiet for:
- `sc.exe query` of an existing service;
- `Get-Service` inspection;
- create/delete of `PT-2026-012-Benign` without starting it.

The final control still generated SCM `7045`, proving that service creation by itself does not satisfy the process-lineage detection.

## Deviation and correction
The first custom-input attempt used nested quoting. SCM created, started, and deleted the temporary service, but no marker was produced. Execution stopped immediately. Cleanup proved no residue. A regression test was added before the fix; the minimum correction removed nested quoting and added durable completion records. The successful positive runs above are the evidence used for validation.

Splunk was also found inactive during preflight. It was restored, all expected listeners were verified, and fresh victim telemetry was confirmed before any Atomic execution.

## Cleanup and postflight
At `2026-07-29T17:00:32.526197Z`:
- no test services remained;
- no marker or completion files remained;
- the victim domain secure channel passed;
- Sysmon, Splunk Forwarder, Velociraptor, Wazuh, and Defender were running;
- the domain controller remained healthy and `dcdiag /q` was quiet.
