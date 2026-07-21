# Cyber lab assessment

## Status boundary

This is a sanitized historical assessment. It does not prove current service health. Exact hostnames, addresses, VM identifiers, domain names, interfaces, ports, firewall rules, connector identifiers, snapshots, and storage paths remain in private operator records.

| Plane | Sanitized historical status | Current claim |
|---|---|---|
| Segmentation and routing | Lab roles were segmented across management, identity, enterprise, testing, and evidence networks | Revalidate before use |
| Identity | Domain services and endpoint trust were previously healthy | Revalidate identity and time before use |
| SIEM | Windows and network telemetry were previously ingested | Revalidate storage, parsers, field mappings, and forwarding |
| Endpoint telemetry | Sysmon, PowerShell, and Windows event sources were previously observed | Revalidate expected event IDs and fields per scenario |
| Network telemetry | IDS telemetry was previously available | Coverage and tuning require a fresh check |
| DFIR | A dedicated collection role and endpoint clients were previously available | Revalidate enrollment, access, storage, and evidence integrity |
| CTI | Advisory enrichment architecture exists | Provider reachability and confidence remain runtime concerns |
| Orchestration | Broker, relay, and receiver components exist | Credentials and endpoints remain private runtime configuration |
| Recovery | Snapshot-based rollback was used historically | Confirm a fresh rollback point before every live scenario |

## Role architecture

```text
management plane
  -> identity services
  -> authorized lab endpoint
  -> internal SIEM service
  -> DFIR workstation / external evidence storage
  -> authorized test runner
```

Infrastructure services are not attack targets. The authorized test runner should primarily target the designated lab endpoint. Identity services require separate, explicit approval even for low-risk validation.

## Required live preflight

A live run is blocked unless a private attestation confirms:

- target role and identity;
- explicit authorization;
- DNS and name resolution;
- time synchronization;
- storage and retention health;
- expected telemetry and SIEM ingestion;
- rollback snapshot availability;
- scenario-specific expected events;
- cleanup steps and timeout;
- an unexpired approval window.

See `schemas/live-preflight.schema.json` and `automation/validators/LIVE_ADAPTER.md`.

## Evidence handling

- Raw event logs, full commands, user identifiers, host identifiers, connector IDs, and live configuration are not committed.
- Runtime evidence belongs in approved external DFIR storage.
- Public validation records retain status, timestamps, hashes, cleanup state, limitations, and sanitized role labels only.
- A historical `validated` label must include a timestamp and must never be interpreted as current health.

## Known limitations

- Splunk field normalization and CIM alignment remain incomplete.
- Elastic EQL and ES|QL outputs are conversion-only until separately validated.
- Velociraptor collection needs an external adapter and artifact-level result contract.
- Canned hunt output must be replaced with a bounded SIEM adapter.
- The workflow does not execute automatic containment.
