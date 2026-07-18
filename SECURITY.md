# Security Policy

## Scope

This repository contains public-safe security engineering content, validation evidence, and generated detection artifacts. The main risks are:
- publishing sensitive environment details in examples
- committing secrets or private telemetry
- overstating lab validation as production assurance

## Reporting

If you find a security issue, avoid posting sensitive details publicly first.

Open a minimal GitHub issue labeled `security` if no private reporting path exists, and omit secrets, tokens, credentials, and environment-specific details.

## Expectations before merge

- remove secrets, tokens, credentials, and private host details
- confirm examples and evidence are safe for public release
- keep generated content clearly labeled as generated
- verify that Markdown still renders and links correctly
- do not fabricate evidence to make the repository look more complete

## Non-goals

This repository does **not** claim production deployment readiness, production alert coverage, or safe offensive execution outside the approved lab scope.
