# Evidence handling

## Evidence boundary

Raw evidence is private. Full disk or memory images, event-log exports, packet captures, credentials, tokens, personal data, and sensitive infrastructure details must not be committed. Public repository artifacts are sanitized derivatives, not the evidence store.

## Handling principles

- collect only within documented authorization and scope
- preserve originals as read-only whenever practical
- calculate and record cryptographic hashes at collection and after transfer
- use stable evidence identifiers instead of embedding sensitive paths or values in public notes
- record collector, date and time, source, method, tool and version, destination, and transfer history
- keep analysis copies separate from originals
- normalize displayed time while retaining the source timestamp and timezone
- document redaction and sanitization decisions
- never alter an original to make publication easier

## Evidence ledger fields

| Field | Purpose |
|---|---|
| Evidence ID | Stable reference used throughout the investigation |
| Description | What the item contains and why it was collected |
| Source | System, account, sensor, or service of origin |
| Acquisition time | Timestamp and timezone of collection |
| Method and tool | Reproducible acquisition details |
| Hash | Integrity value for the collected item |
| Custody location | Private storage reference, never secret material itself |
| Access or transfer history | Who handled the item and when |
| Public derivative | Sanitized excerpt, query result, or timeline row, if published |

## Publication review

Before publishing, remove or generalize secrets, personal data, internal addressing, tenant or account identifiers, hostnames where sensitive, and unrelated third-party data. Verify that sanitization does not change the meaning of the cited observation. If a safe derivative cannot preserve that meaning, document the conclusion at a higher level and keep the source private.
