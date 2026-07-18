# Contributing

Thanks for improving `cybersecurity-playbook`.

## Contribution goals

This repo should stay:
- technically accurate
- public-safe
- evidence-backed
- understandable to both engineers and hiring managers
- clearly scoped as the companion content repository for DetLab-DAC

## Good contributions

- stronger scenario definitions
- higher-quality Sigma rules
- better positive/negative fixtures
- clearer hunt and investigation documentation
- validation automation improvements
- documentation that improves navigation without reducing technical depth

## Avoid

- unsupported vendor claims
- fabricated detections, alerts, logs, or screenshots
- committing secrets, tokens, tenant names, or sensitive internal details
- blurring the line between canonical authored content and generated output
- presenting lab validation as production proof

## Workflow

1. create a focused branch
2. keep changes scoped and reviewable
3. run repository validation before opening a PR
4. explain the technical change and the evidence behind it

## Validation commands

```bash
python3 playbook validate
python3 playbook --json sigma lint
python3 playbook --json sigma convert --target all
python3 playbook --json test fixtures
python3 playbook --json validate previous-scenarios
python3 automation/validators/check_markdown.py
```

## Content rules

- Edit canonical authored content in `purple-team/`, `detections/sigma/`, `docs/`, `templates/`, and `tests/fixtures/`.
- Do **not** hand-edit generated queries in `detections/generated/`; regenerate them from Sigma.
- Keep live-validation records sanitized and tied to real evidence.
- When a rule is only fixture-tested or conversion-supported, say so explicitly.
