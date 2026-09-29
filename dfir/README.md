# DFIR capability library

This directory documents reusable digital-forensics and incident-response methods that support investigation-led case work. It does not contain raw evidence.

## Capability maturity

| Capability | Status | Index |
|---|---|---|
| Targeted forensic acquisition | **Planned** | [Acquisition](acquisition/README.md) |
| Timeline generation and analysis | **Planned** | [Timelines](timelines/README.md) |
| Memory acquisition and triage | **Planned** | [Memory](memory/README.md) |
| Public sanitization and public-safe derivation | **Verified** | [Evidence handling](evidence-handling/README.md) |
| End-to-end private evidence handling | **Installed** | [Evidence handling](evidence-handling/README.md) |

Statuses use **Planned**, **Installed**, **Verified**, and **Live validated** for capability maturity. They do not change Sigma-native rule lifecycle values.

## Operating boundary

Raw acquisitions and sensitive evidence remain in approved private storage. Repository content should describe method, provenance, integrity checks, sanitized observations, and limitations. Start with the [investigation lifecycle](../docs/workflows/investigation-lifecycle.md) and use the [investigation template](../templates/investigation-template.md) for case records.
