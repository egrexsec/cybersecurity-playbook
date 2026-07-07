# Security Policy

## Scope

This repository mainly stores public markdown content and templates. The biggest security risks are:
- publishing sensitive environment details in examples
- committing secrets or internal detection logic
- sharing screenshots or artifacts with customer or tenant data

## Reporting

If you find a security issue, avoid posting sensitive details publicly first.

Open a minimal GitHub issue labeled `security` if no private reporting path exists, and omit secrets, tokens, and environment-specific detail.

## Expectations

Before merging:
- remove tenant names, secrets, tokens, and hostnames
- confirm examples are safe for public release
- verify markdown still renders as expected
