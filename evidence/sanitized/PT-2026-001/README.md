# PT-2026-001 Sanitized Evidence Pack

This directory contains **sanitized, text-only** execution records for the first Mayuri purple-team milestone.

## Included records
- `positive_atomic.json` / `positive_atomic_validation.json`
- `positive_variant.json` / `positive_variant_validation.json`
- `negative_get_date.json` / `negative_get_date_validation2.json`
- `negative_get_process.json` / `negative_get_process_validation.json`

## What is intentionally excluded
- raw EVTX exports
- full memory captures
- packet captures
- credentials, tokens, secrets, or API configs
- large binaries and raw acquisitions

## Evidence notes
- Files are suitable for a public portfolio repository because they preserve the workflow and outcomes without embedding sensitive infrastructure details or large raw data.
- The validation files are the canonical records for custom Wazuh rule outcomes.

## SHA256
- `5e5ee9546c2e24316f12731332c9b971b56ac12fc33250c018090293f5630054` `negative_get_date.json`
- `310f836bfd1b741073639549e84443bf8bfa13d3a69a2d59985c62d3ee7df21e` `negative_get_date_validation2.json`
- `b6642b2bc776200f1e12f961142ecdb9a7648ce496cd502337450c9f9e50fde9` `negative_get_date_validation.json`
- `8d674ea65b6f743253fd03e0e62f44f3530bd6708063170df689c2e245b2ad4d` `negative_get_process.json`
- `88f9f0413177659180b1847df78677c503a859228f844054c720bbd81e9e399f` `negative_get_process_validation.json`
- `8eee9f28c9567403e1cb13354422f4918f46d2ed5941db26f5c0eff7b4951853` `positive_atomic.json`
- `e73b9cecfa6115907f5ca63315e1283d54ff9afa3aa7f14c7d527de2e602c958` `positive_atomic_validation.json`
- `b8c0b66e7313988ee0ca2cea38cd8872a7e9b73c28b6d19c7cacf8cb8b9ab57a` `positive_variant.json`
- `de8451644b6128e84f0229a243516c5e108c5f508f652c2ca024cc37c42a78f4` `positive_variant_validation.json`
