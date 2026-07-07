# cybersecurity-playbook

Companion content repository for **DetLab-DAC**. This repo stores reusable security documentation, templates, and playbook content that can support detection engineering, hunting, investigation, and response work without pretending to be a separate platform.

## Project summary

`cybersecurity-playbook` is a markdown-first content repo for reusable security material. It complements DetLab-DAC by holding templates, sample detections, structured notes, and platform-specific content that teams can adapt into their own workflows.

## Who it is for

- detection engineers
- threat hunters
- SOC analysts
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

## Features

- markdown-first authoring
- structured frontmatter examples
- reusable templates for multiple security-content types
- simple directory organization by domain/source
- easy Git review and reuse

## Architecture

```text
templates/               Reusable authoring templates
mde/                     Microsoft Defender / Advanced Hunting examples
aws/                     AWS-oriented content examples
velociraptor/            Velociraptor notes and artifact references
```

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

## Usage

Typical workflow:
1. pick a template from `templates/`
2. copy it into the target domain folder
3. adapt telemetry, ATT&CK, triage, and investigation content to your environment
4. review it in Git like any other content artifact
5. reference or import the resulting content into DetLab-DAC or your internal documentation flow

## Project structure

```text
templates/
  detlab-detection-template.md
  hunt-template.md
  investigation-template.md
  kql-template.md
  velociraptor-template.md
mde/
aws/
velociraptor/
```

## Testing

There is no automated test suite in this repository today.

Current validation is content-focused:
- review markdown rendering
- validate structure and frontmatter manually
- check cross-references before merge

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
