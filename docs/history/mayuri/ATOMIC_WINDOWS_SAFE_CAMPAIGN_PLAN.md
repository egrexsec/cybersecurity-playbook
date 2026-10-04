# Atomic Red Team Windows-Safe Persistence/Execution Campaign Plan

## Scope decision
User-approved scope:
- run **Windows-safe persistence/execution techniques only**
- validate **per technique**
- require **cleanup** after each technique

## Current evidence-based inventory
- Atomic Red Team Windows-capable techniques with `command_prompt` and/or `powershell` executors on the victim: **74**
- Live-validated Mayuri techniques: **12**
- Broad inventory coverage: **16.2%**

Validated techniques:
- `T1059.001` PowerShell
- `T1059.003` Windows Command Shell
- `T1047` Windows Management Instrumentation
- `T1053.005` Scheduled Task
- `T1543.003` Windows Service Creation
- `T1547.001` Registry Run Keys / Startup Folder
- `T1037.001` Logon Script
- `T1197` BITS Jobs
- `T1546.013` PowerShell Profile
- `T1218.011` Rundll32
- `T1218.010` Regsvr32
- `T1569.002` Service Execution

## Safety stance
This campaign must **not** be run as one firehose batch. Each technique requires:
1. preflight
2. low-risk positive variant selection
3. benign negatives
4. local/central telemetry confirmation
5. cleanup verification
6. repository artifact update

## Completed batches
The 12 techniques listed above are live validated. Historical evidence does not replace fresh preflight or current health checks for later batches.

## Candidate backlog
Candidates require a fresh safety review before selection:
- `T1546.003` WMI Event Subscription
- `T1546.011` Application Shimming
- `T1547.009` Shortcut Modification
- `T1127.001` MSBuild

## Exclusions for now
Defer techniques that are destructive, environment-sensitive, or likely to destabilize the victim/DC path until a dedicated approval gate exists:
- account manipulation families
- authentication-process modification families
- LSASS / SSP / password-filter persistence
- firmware, driver, or kernel-level persistence
- Office/Outlook persistence requiring additional operator/UI setup
- externally dependent or lateral-movement-heavy families unless explicitly approved

## Execution standard per technique
For each technique:
- one scenario ID
- one Sigma rule
- Splunk conversion
- at least two positive variants where feasible
- at least three negative tests
- one live validation JSON record
- one detection validation markdown
- one hunt hypothesis
- one cleanup script

## Next action
Select the next candidate only after reviewing its exact upstream Atomic definitions, prerequisites, commands, cleanup, and host-impact profile. Continue one technique at a time on the approved victim.
