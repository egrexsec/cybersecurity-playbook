# cybersecurity-playbook

Companion content repository for **DetLab-DAC**. This repo stores reusable security documentation, templates, and playbook content for detection engineering, hunting, investigation, and response work without pretending to be a separate platform.

## Project summary

`cybersecurity-playbook` is a markdown-first content library for reusable security material. It complements DetLab-DAC by holding templates, sample detections, structured notes, and platform-specific content that teams can adapt into their own workflows.

## Start here

| Need | Go to | Use it for |
| --- | --- | --- |
| Write a detection brief | `templates/detlab-detection-template.md` | Canonical detection content for DetLab-DAC |
| Write a hunt | `templates/hunt-template.md` | Hypothesis, telemetry, query, and follow-up structure |
| Document an investigation | `templates/investigation-template.md` | Case notes, timeline, evidence, and outcome tracking |
| Draft MDE Advanced Hunting content | `templates/kql-template.md` and `mde/` | KQL examples and Microsoft Defender content |
| Capture Velociraptor work | `templates/velociraptor-template.md` and `velociraptor/` | Artifact notes and endpoint collection guidance |
| Review AWS lab examples | `aws/` | Cloud-security investigation and learning content |

## Who it is for

- detection engineers
- threat hunters
- SOC analysts
- DFIR practitioners
- defenders building internal markdown-based knowledge bases
- contributors who want reusable security-content building blocks separate from app code

## Problem it solves

Security teams often need reusable content before they need another application. This repo provides structured, editable markdown artifacts that can be copied into playbooks, notes, detections, investigations, and validation workflows.

## Current status

**Active companion repository.**

Confirmed in the repository today:
- markdown templates for detections, hunts, investigations, KQL, and Velociraptor content
- MDE Advanced Hunting detection examples
- AWS FLAWS2-oriented content examples
- Velociraptor artifact notes

## What it contains

- detection templates
- hunt templates
- investigation templates
- KQL templates
- Velociraptor templates
- reusable markdown standards for structured security content
- sample content that can feed or complement DetLab-DAC

## What it is not

- not a competing standalone platform
- not a SIEM or case-management product
- not an automated detection deployment system
- not a replacement for environment-specific engineering review

## Repository map

```text
templates/               Reusable authoring templates
mde/                     Microsoft Defender / Advanced Hunting examples
aws/                     AWS-oriented lab and investigation examples
velociraptor/            Velociraptor notes and artifact references
```

## Recommended workflow

1. Pick the closest template from `templates/`.
2. Copy it into the target domain folder.
3. Adapt telemetry, ATT&CK, triage, validation, and response content to the environment.
4. Keep examples public-safe: no tenant names, secrets, customer hostnames, or private telemetry.
5. Review it in Git like any other content artifact.
6. Reference or import the resulting content into DetLab-DAC or an internal documentation flow.

## Features

- markdown-first authoring
- structured frontmatter examples
- reusable templates for multiple security-content types
- simple directory organization by domain/source
- easy Git review and reuse
- companion content model for DetLab-DAC

## Tech stack

- Markdown
- YAML frontmatter conventions
- Git / GitHub review workflow

## Quick start

```bash
git clone https://github.com/egrexsec/cybersecurity-playbook.git
cd cybersecurity-playbook
```

Open the markdown files in your editor of choice.

## Testing

There is no automated test suite in this repository today.

Current validation is content-focused:
- review markdown rendering
- validate structure and frontmatter manually
- check cross-references before merge
- confirm examples are sanitized for public release

## Deployment

No application deployment is required. This is a content repository.

## Roadmap

See [ROADMAP.md](ROADMAP.md).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Security

See [SECURITY.md](SECURITY.md).

## License

This repository includes a [LICENSE](LICENSE) file.
