# Sigma to Splunk Field Mapping

## Current-state note
The live Splunk environment ingests Windows data primarily as `XmlWinEventLog:*` sources. Official Sigma conversion works syntactically, but live execution currently depends on matching `_raw` XML because equivalent extracted fields/CIM mappings are not yet normalized in the lab.

## Verified mappings used now
| Sigma field | Current live Splunk representation | Sourcetype / source | Verified | Notes |
|---|---|---|---|---|
| `ScriptBlockText` | `_raw` XML `<Data Name='ScriptBlockText'>...` | `XmlWinEventLog:Microsoft-Windows-PowerShell/Operational` | Yes | used by PT-2026-001 and PT-2026-003 |
| `Image` | `_raw` XML `<Data Name='Image'>...` | `XmlWinEventLog:Microsoft-Windows-Sysmon/Operational` | Yes | used by PT-2026-002 |
| `CommandLine` | `_raw` XML `<Data Name='CommandLine'>...` | `XmlWinEventLog:Microsoft-Windows-Sysmon/Operational` | Yes | used by PT-2026-002 |
| `ParentImage` | `_raw` XML `<Data Name='ParentImage'>...` | `XmlWinEventLog:Microsoft-Windows-Sysmon/Operational` | Yes | present in raw events; not yet used by current Sigma live queries |
| `User` | `_raw` XML `<Data Name='User'>...` | Sysmon / PowerShell XML | Yes | verified in raw event samples |
| `EventID` | `_raw` XML `<EventID>...</EventID>` | XML event body | Yes | base search constrains event family |
| `Channel` | `source` plus XML `<Channel>...</Channel>` | XML event body | Yes | fixture and sanitized historical mappings use `source=` first |
| `host` | Splunk `host` field | all ingested Windows telemetry | Yes | authorized endpoint and identity-service roles were historically observed |

## Official-field mapping target state
| Sigma field | Desired Splunk field | CIM candidate | Current status |
|---|---|---|---|
| `Image` | `Image` | `process_path` | Partially ready |
| `CommandLine` | `CommandLine` | `process` | Partially ready |
| `ParentImage` | `ParentImage` | `parent_process_path` | Partially ready |
| `User` | `User` | `user` | Partially ready |
| `EventID` | `EventCode` or `EventID` | `signature_id` | Partially ready |
| `ScriptBlockText` | `ScriptBlockText` | N/A | Partially ready |

## Pipeline stance
- **Official portability pipeline**: use pySigma Splunk backend with `windows-logsources`
- **Current live validation pipeline**: use generated Mayuri raw-XML Splunk queries under `detections/generated/splunk/live/`
- **Do not** claim CIM-backed portability until actual field extraction is normalized and revalidated live
