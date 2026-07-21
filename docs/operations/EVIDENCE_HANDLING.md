# Evidence Handling

## Objectives
- preserve raw evidence immutability
- separate raw, processed, and sanitized outputs
- record SHA-256 hashes
- record tool versions and UTC timestamps
- prevent secrets or large raw evidence from entering GitHub

## Recommended storage pattern

```text
DFIR storage/
├── raw/
│   └── <case-id>/
├── processed/
│   └── <case-id>/
└── exports/
    └── <case-id>/
```

## Rules
1. Raw evidence becomes read-only immediately after collection.
2. Processed evidence is derived material only.
3. Sanitized exports are the only evidence form intended for the public repository.
4. Every collection must produce:
   - manifest id
   - collector/tool name
   - version
   - started/completed timestamps in UTC
   - file list
   - SHA-256 hashes
   - error list
5. AI output must never modify raw evidence.
6. No automatic evidence deletion without explicit approval.

## Repo mapping
- raw evidence location: external DFIR storage only
- processed references: `investigations/cases/<case-id>/evidence-manifest.json`
- sanitized repo evidence: `evidence/sanitized/<case-id>/`
- evidence manifests: `evidence/manifests/`

## Permissions guidance
- raw: analyst/DFIR-only, read-only after write
- processed: restricted analyst access
- sanitized: repo-safe after review

## Disk and retention
- monitor DFIR disk headroom before large collections
- retain raw evidence based on case policy, not convenience
- never assume repository history is a raw-evidence retention system
