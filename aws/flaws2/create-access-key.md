---
id: DET-3201
name: AWS CreateAccessKey
content_kind: investigation
status: validated
severity: high
author: mell0wx
domain:
  - cloud
platforms:
  - aws
logsource:
  product: aws
  service: cloudtrail
attack:
  technique: T1098
  tactic: persistence
attack_context:
  - technique: T1078
    tactic: defense-evasion
    name: Valid Accounts
    coverage: related
    rationale: Access key creation often extends use of already compromised IAM principals.
  - technique: T1530
    tactic: collection
    name: Data from Cloud Storage
    coverage: gap
    rationale: Key creation may be followed by S3 discovery or exfiltration not directly visible here.
data_sources:
  - name: CloudTrail
    kind: cloud
    provider: aws
    event_names:
      - CreateAccessKey
  - name: IAM credential report
    kind: identity
    provider: aws
triage_steps:
  - step: Validate who created the key, for which IAM user, and from what source IP and session context.
    priority: high
  - step: Determine whether the principal normally performs IAM administration and whether MFA or federation was present.
    priority: high
investigation_steps:
  - step: Review nearby IAM activity including CreateUser, AttachUserPolicy, PutUserPolicy, and AssumeRole.
    priority: high
  - step: Trace first use of the new access key across CloudTrail to identify discovery, privilege escalation, or collection activity.
    priority: high
falsepositives:
  - Expected IAM administration during user onboarding or access rotation.
artifacts:
  - name: CloudTrail CreateAccessKey event
    category: cloud_log
    path: CloudTrail
  - name: IAM user metadata and credential age
    category: identity_log
    path: IAM
cloud_telemetry:
  - provider: aws
    source: CloudTrail
    event_names:
      - CreateAccessKey
      - ListAccessKeys
      - UpdateAccessKey
      - DeleteAccessKey
      - AttachUserPolicy
      - PutUserPolicy
    notes: Review the full IAM change window before and after key creation.
response_actions:
  - title: Disable or delete the new key if it cannot be tied to approved IAM administration.
    priority: high
  - title: Rotate related credentials and review the creating principal for broader compromise.
    priority: high
references:
  - https://attack.mitre.org/techniques/T1098/
tests:
  - name: Analyst validation
    source: markdown-curation
    test_id: aws-create-access-key-v1
---

# AWS CreateAccessKey

Treats access-key creation as a detection-first cloud investigation so analysts can quickly assess whether IAM persistence was established through a valid but suspicious principal.

## Query

```text
CloudTrail EventName=CreateAccessKey
Pivot fields: userIdentity.arn, requestParameters.userName, sourceIPAddress, userAgent, accessKey.accessKeyId
```

## Triage Guidance

- Confirm whether the key was created for the acting identity or for a different IAM user.
- Review console sign-in, federation, and MFA context around the creating session.

## Investigation Steps

- Trace first use of the new access key and compare it with the source IP and user agent that created it.
- Review policy changes, role assumptions, and storage access shortly after creation.

## False Positives

- Planned access rotation or break-glass user provisioning.

## Artifacts

- CloudTrail event history
- IAM user metadata
- Credential report snapshots

## Response Actions

- Disable the key immediately if ownership or business justification cannot be established.
