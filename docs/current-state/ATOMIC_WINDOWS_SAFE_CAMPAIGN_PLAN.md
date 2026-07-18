# Atomic Red Team Windows-Safe Persistence/Execution Campaign Plan

## Scope decision
User-approved scope:
- run **Windows-safe persistence/execution techniques only**
- validate **per technique**
- require **cleanup** after each technique

## Current evidence-based inventory
- Atomic Red Team Windows-capable techniques with `command_prompt` and/or `powershell` executors on the victim: **74**
- Of those, already validated in Mayuri:
  - `T1059.001` PowerShell
  - `T1059.003` Windows Command Shell
  - `T1047` Windows Management Instrumentation
  - `T1053.005` Scheduled Task

## Safety stance
This campaign must **not** be run as one firehose batch.
Each technique requires:
1. preflight
2. low-risk positive variant selection
3. benign negatives
4. local/central telemetry confirmation
5. cleanup verification
6. repo artifact update

## Batch order
### Completed
- `T1059.001`
- `T1059.003`
- `T1047`
- `T1053.005`

### Next priority batch
1. `T1543.003` Windows Service
2. `T1569.002` Service Execution
3. `T1547.001` Registry Run Keys / Startup Folder
4. `T1037.001` Logon Script (Windows)

### Later persistence/execution candidates
- `T1546.003` WMI Event Subscription
- `T1546.013` PowerShell Profile
- `T1546.011` Application Shimming
- `T1547.009` Shortcut Modification
- `T1197` BITS Jobs
- `T1218.011` Rundll32
- `T1127.001` MSBuild

## Exclusions for now
Defer techniques that are too destructive, too environment-sensitive, or likely to destabilize the victim/DC path until a dedicated approval gate exists. Examples:
- account manipulation families
- auth-process modification families
- LSASS / SSP / password-filter persistence
- firmware / driver / kernel-level persistence
- Office/Outlook persistence requiring additional operator/UI setup
- externally dependent or lateral-movement-heavy families unless explicitly approved

## Execution standard per technique
For each technique:
- one scenario ID
- one Sigma rule
- Splunk conversion
- at least 2 positive variants where feasible
- at least 3 negative tests
- one live validation JSON record
- one detection validation markdown
- one hunt hypothesis update
- one cleanup script

## Immediate next action
Proceed with:
- `T1543.003` Windows Service

Reason:
- it is the closest persistence neighbor to the now-validated scheduled-task path
- it has clear Windows-native telemetry
- it fits the existing Mayuri validation workflow
