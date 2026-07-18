# PT-2026-002 Sanitized Evidence Pack

This directory contains **sanitized, text-only** validation records for the Windows Command Shell scenario.

## Included records
- `positive_batch_validation.json`
- `positive_variant_validation.json`
- `negative_dir_validation.json`
- `negative_echo_validation.json`

## Notes
- Files preserve command outcomes and alert hits without publishing raw EVTX, memory, or packet-capture artifacts.
- The positive records include marker-file confirmation and matching Wazuh detections.
- The negative records confirm that the custom PT-specific rules stayed quiet during benign command-shell use.
