# Telemetry Analysis

## Relevant sources
- PowerShell Operational event IDs `4103` and `4104`
- Sysmon Event ID `1` process creation
- supporting Wazuh built-ins for the historical rule path

## Splunk investigation approach
The current lab uses Splunk as the primary live validation backend. The repo currently supports:
- canonical Sigma conversion to Splunk SPL
- generated live Splunk queries for the current lab field model

## Important observed fields
- `ScriptBlockText`
- `CommandLine`
- `Image`
- `ParentImage`
- `User`

## Timeline observations
The PT-2026-001 validation path records:
- original positive execution
- modified variant execution
- benign negative checks
- cleanup confirmation

## Current limitation
Field normalization is still incomplete in the live Splunk environment, so some live validation relies on raw XML-backed matching rather than a fully normalized CIM field layer.
