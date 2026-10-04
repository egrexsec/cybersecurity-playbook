# Detection Content Specification v1

This repository retains the former **DetLab Detection Content Specification v1** locally at:

- `schemas/detlab-detection-content-v1.schema.json`

The schema identifier remains `https://schemas.detlab.dev/detection-content/v1.0.0/schema.json` for compatibility with committed artifacts. The retired `DetLab-DAC` repository is not a runtime, build, or documentation dependency.

## Contract boundary

The v1 contract is a portable, normalized interchange model. It does **not** replace the authored source format:

- Sigma YAML remains canonical in `cybersecurity-playbook`.
- The locally retained adapter normalizes authored Sigma into the v1 shape.
- Splunk, Elastic, Kusto, and other target queries are derived artifacts, never competing authored sources.

Historical DetLab fields and names remain where changing them would break artifact provenance or compatibility. Current validation and generation operate entirely inside `cybersecurity-playbook`.

## Required normalized fields

- identity: `spec_version`, `kind`, `id`, `title`, `description`
- lifecycle: `status`, `severity`, `authors`
- behavior: `platforms`, `attack`, `logsource`, `logic`
- canonical source provenance: `source.format`, `source.path`, `source.sha256`, `source.canonical`

`logic.body` contains selections. `logic.condition` remains explicit so consumers do not need format-specific condition discovery.

## Generated artifact provenance

Every generated artifact records:

- target and query language
- rendered content and its SHA-256
- canonical source SHA-256
- contract version
- converter package name and version

An artifact is stale when its recorded source hash or contract version no longer matches the normalized canonical source.

## Repository adapter

`automation/validators/detection_content_spec.py` normalizes authored Sigma rules and provides provenance/staleness helpers.

Tests:

```bash
python3 -m unittest tests.test_detection_content_spec -v
```

The full CI test discovery executes these tests automatically.
