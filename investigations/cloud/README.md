# Cloud investigations

**Capability maturity: Verified (AWS CloudTrail workflow)**

AWS is an active investigation domain in this portfolio. The current verified capability comes from bounded public training data rather than a standing owned cloud range.

## Verified scope

The Flaws2.cloud Defender track exercised:

- AWS CLI identity and named-profile usage
- CloudTrail log retrieval from S3
- recursive local analysis with PowerShell and `jq`
- chronological timeline construction
- source IP, principal, account, event, and user-agent correlation
- IAM / STS pivots around suspicious activity
- credential-theft identification
- ECR repository-policy review
- understanding Athena as a scalable alternative for querying CloudTrail in S3

## Intended reusable scope

- CloudTrail-centered activity reconstruction
- IAM principal, role, policy, and session analysis
- control-plane and data-plane timeline correlation
- resource-policy review
- evidence preservation for exported cloud logs and configuration snapshots
- detection opportunities derived from completed investigations

## Current boundary

No standing AWS lab is provisioned or implied by this repository. Future cloud cases should use approved owned environments or bounded training datasets and must preserve provenance, scope, and public-safe handling.

See the [Flaws2.cloud Defender case study](../../case-studies/aws/flaws2-defender/README.md).
