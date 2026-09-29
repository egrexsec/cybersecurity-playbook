# Forensic acquisition

## Objective

Acquire the minimum evidence needed to answer the scoped question while preserving integrity, provenance, and operational safety.

## Pre-acquisition record

- authorization, case identifier, owner, and target
- collection objective and expected evidence sources
- volatility order and business-impact constraints
- system time, timezone, and known clock offsets
- available storage, encryption, and private custody location
- approved tooling and versions
- stop conditions and escalation path

## Acquisition sequence

1. Record the live system context before collection.
2. Prioritize volatile evidence when its value and authorization justify the risk.
3. Capture targeted endpoint, identity, network, or cloud artifacts before broad acquisition.
4. Record every command, collector, filter, and time window used.
5. Hash collected files and verify integrity after transfer.
6. Store originals privately and perform analysis on working copies.
7. Note failures, partial collections, overwritten artifacts, and retention gaps.
8. Produce only sanitized derivatives for this repository.

## Collection tiers

| Tier | Examples | Typical use |
|---|---|---|
| Triage | process, network, login, autorun, and recent event data | establish scope and guide pivots |
| Targeted | selected event logs, registry hives, task definitions, service data, browser or execution artifacts | test a defined hypothesis |
| Full | disk image, memory image, broad cloud export | complex or high-impact cases with explicit need and storage controls |

Acquisition is not complete because a tool returned success. Verify expected artifacts, sizes or record counts where safe, hashes, timestamps, and readability before analysis.
