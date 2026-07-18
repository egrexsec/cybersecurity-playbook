# Purple-Team to Detection Workflow

## Goal
Create a repeatable path from approved emulation to validated detection.

## First implementation path
1. Validate scope, target, snapshots, time, telemetry, and cleanup.
2. Capture a telemetry baseline.
3. Execute an approved low-risk scenario.
4. Collect Windows event, process, and targeted DFIR evidence.
5. Develop hunt queries from observed behavior.
6. Build a portable Sigma rule.
7. Translate into the active SIEM test scope.
8. Replay positive, variant, and negative tests.
9. Record latency, matching fields, and gaps.
10. Commit only sanitized evidence and documentation.

## Safety requirements
- Fail closed on missing prerequisites.
- Keep execution on approved hosts only.
- Use reversible tests with explicit cleanup.
- Never commit raw credentials or large raw acquisitions.
