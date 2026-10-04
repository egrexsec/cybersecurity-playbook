# Flaws2.cloud Defender Track — Windows PowerShell Notes

## Overview

I completed the **Flaws2.cloud Defender Track** from a Windows environment using **PowerShell, AWS CLI, and `jq`**.

The track focused on practical AWS security investigation skills:

1. Download CloudTrail logs
2. Access the target account
3. Analyze logs with `jq`
4. Identify credential theft
5. Identify a public resource
6. Understand how Athena can scale the same analysis

The biggest takeaway was learning how to move from raw AWS activity into a structured investigation timeline and then pivot from suspicious events into identities, credentials, and resource configuration.

> **Validation boundary:** This case used the bounded public Flaws2.cloud Defender training dataset and workflow. It verifies the analysis method; it is not a claim of live validation in a standing owned AWS range.

---

# Objective 1 — Download CloudTrail Logs

## Key takeaway

The first step was getting the AWS CLI configured correctly and downloading the CloudTrail evidence locally.

Verify the active identity:

```powershell
aws sts get-caller-identity
```

List accessible S3 buckets:

```powershell
aws s3 ls
```

Download the CloudTrail logs:

```powershell
aws s3 sync s3://flaws2-logs .
```

### Troubleshooting note

The AWS CLI initially failed with:

```text
Could not connect to the endpoint URL:
"https://sts.None.amazonaws.com/"
```

The cause was a missing AWS region.

Setting the default region to:

```text
us-east-1
```

resolved the issue.

---

# Objective 2 — Access the Target Account

## Key takeaway

This objective reinforced the importance of **AWS identities and profiles**.

Instead of treating credentials as generic access, the investigation required understanding:

- which account was being accessed
- which identity was active
- which profile represented that identity
- what permissions that identity had

Using named AWS CLI profiles made it easier to keep identities separate.

Example:

```powershell
aws --profile target_security sts get-caller-identity
```

This became important later when pivoting into the compromised account and querying ECR configuration.

---

# Objective 3 — Analyze CloudTrail with `jq`

This was the most useful objective for building a repeatable Windows investigation workflow.

The original lab assumes Linux/macOS, so I translated the workflow into **PowerShell pipelines**.

## Recursively process CloudTrail JSON

Basic JSON formatting:

```powershell
Get-ChildItem -Recurse -File -Filter *.json |
    ForEach-Object { Get-Content -Raw $_.FullName } |
    jq '.'
```

This confirmed that the downloaded files contained valid CloudTrail records.

## Show only event names

```powershell
Get-ChildItem -Recurse -File -Filter *.json |
    ForEach-Object { Get-Content -Raw $_.FullName } |
    jq '.Records[] | .eventName'
```

This provided a quick view of AWS API activity such as:

```text
GetObject
ListBuckets
AssumeRole
GetDownloadUrlForLayer
```

## Build a basic chronological timeline

```powershell
Get-ChildItem -Recurse -File -Filter *.json |
    ForEach-Object { Get-Content -Raw $_.FullName } |
    jq -cr '.Records[] | [.eventTime, .eventName] | @tsv' |
    Sort-Object
```

This was useful for reconstructing events in chronological order.

## Build a detailed investigation timeline

```powershell
Get-ChildItem -Recurse -File -Filter *.json |
    ForEach-Object { Get-Content -Raw $_.FullName } |
    jq -cr '.Records[] | [.eventTime, .sourceIPAddress, .userIdentity.arn, .userIdentity.accountId, .userIdentity.type, .eventName] | @tsv' |
    Sort-Object
```

Fields included:

- event time
- source IP
- user ARN
- account ID
- user type
- event name

This became the core investigation view.

## Export timeline to spreadsheet

```powershell
Get-ChildItem -Recurse -File -Filter *.json |
    ForEach-Object { Get-Content -Raw $_.FullName } |
    jq -cr '.Records[] | [.eventTime, .sourceIPAddress, .userIdentity.arn, .userIdentity.accountId, .userIdentity.type, .eventName] | @tsv' |
    Sort-Object |
    Set-Content .\cloudtrail-timeline.tsv
```

Open it with:

```powershell
Invoke-Item .\cloudtrail-timeline.tsv
```

## Export timeline with headers

```powershell
"eventTime`tSourceIPAddress`tUserArn`tAccountId`tUserType`tEventName" |
    Set-Content .\cloudtrail-timeline.tsv

Get-ChildItem -Recurse -File -Filter *.json |
    ForEach-Object { Get-Content -Raw $_.FullName } |
    jq -cr '.Records[] | [.eventTime, .sourceIPAddress, .userIdentity.arn, .userIdentity.accountId, .userIdentity.type, .eventName] | @tsv' |
    Sort-Object |
    Add-Content .\cloudtrail-timeline.tsv
```

## Add User-Agent data

The `userAgent` field helped distinguish between:

- AWS CLI activity
- browser activity
- AWS service activity
- other clients or SDKs

Query:

```powershell
Get-ChildItem -Recurse -File -Filter *.json |
    ForEach-Object { Get-Content -Raw $_.FullName } |
    jq -cr '.Records[] | [.eventTime, .sourceIPAddress, .userIdentity.arn, .userIdentity.accountId, .userIdentity.type, .eventName, .userAgent] | @tsv' |
    Sort-Object
```

Export with headers:

```powershell
"eventTime`tSourceIPAddress`tUserArn`tAccountId`tUserType`tEventName`tUserAgent" |
    Set-Content .\cloudtrail-timeline-useragent.tsv

Get-ChildItem -Recurse -File -Filter *.json |
    ForEach-Object { Get-Content -Raw $_.FullName } |
    jq -cr '.Records[] | [.eventTime, .sourceIPAddress, .userIdentity.arn, .userIdentity.accountId, .userIdentity.type, .eventName, .userAgent] | @tsv' |
    Sort-Object |
    Add-Content .\cloudtrail-timeline-useragent.tsv
```

This was the most useful spreadsheet view for investigation context.

---

# Objective 4 — Identify Credential Theft

## Key takeaway

The investigation moved from general CloudTrail activity into specific suspicious API actions.

One useful filter was isolating `AssumeRole` activity.

```powershell
Get-ChildItem -Recurse -File -Filter *.json |
    ForEach-Object { Get-Content -Raw $_.FullName } |
    jq -cr ".Records[] | select(.eventName == \`"AssumeRole\`")"
```

Compact timeline:

```powershell
Get-ChildItem -Recurse -File -Filter *.json |
    ForEach-Object { Get-Content -Raw $_.FullName } |
    jq -cr ".Records[] | select(.eventName == \`"AssumeRole\`") | [.eventTime, .sourceIPAddress, .userIdentity.arn, .eventName] | @tsv" |
    Sort-Object
```

Another useful event was `ListBuckets`:

```powershell
Get-ChildItem -Recurse -File -Filter *.json |
    ForEach-Object { Get-Content -Raw $_.FullName } |
    jq ".Records[] | select(.eventName == \`"ListBuckets\`")"
```

Compact view:

```powershell
Get-ChildItem -Recurse -File -Filter *.json |
    ForEach-Object { Get-Content -Raw $_.FullName } |
    jq -cr ".Records[] | select(.eventName == \`"ListBuckets\`") | [.eventTime, .sourceIPAddress, .userIdentity.arn, .eventName] | @tsv" |
    Sort-Object
```

### Investigation lesson

The important part was not just finding a suspicious API call.

The useful pivot was correlating:

```text
event
→ timestamp
→ source IP
→ identity
→ user agent
→ surrounding activity
```

That made it possible to distinguish credential misuse from normal AWS service activity.

## Reduce AWS service noise

```powershell
Get-ChildItem -Recurse -File -Filter *.json |
    ForEach-Object { Get-Content -Raw $_.FullName } |
    jq -cr ".Records[] | select(.userIdentity.type != \`"AWSService\`") | [.eventTime, .sourceIPAddress, .userIdentity.type, .eventName] | @tsv" |
    Sort-Object
```

This was useful as an investigative view, but AWS service events should not be deleted or ignored permanently because they can still provide useful context.

---

# Objective 5 — Identify the Public Resource

## Key takeaway

After identifying the credential misuse, the next step was understanding what resource configuration enabled the attack.

The ECR repository policy was retrieved with:

```powershell
aws --profile target_security ecr get-repository-policy --repository-name level2
```

The `policyText` field was returned as escaped JSON.

PowerShell piped the output directly into `jq`:

```powershell
aws --profile target_security ecr get-repository-policy --repository-name level2 |
    jq '.policyText | fromjson'
```

A cleaner view of the relevant policy fields:

```powershell
aws --profile target_security ecr get-repository-policy --repository-name level2 |
    jq '.policyText | fromjson | .Statement[] | {Effect, Principal, Action}'
```

The important finding was:

```json
"Effect": "Allow",
"Principal": "*"
```

The wildcard principal allowed access to the listed ECR read actions.

### Investigation lesson

This demonstrated an important Cloud IR pivot:

```text
Suspicious activity
        ↓
Identity investigation
        ↓
Credential misuse
        ↓
Target resource
        ↓
Resource policy
        ↓
Root cause
```

---

# Objective 6 — Understand Athena for CloudTrail Analysis

I did not recreate the Athena environment in a personal AWS account because the core investigation had already been completed locally.

The important concept was understanding how Athena changes the **scale of analysis**, not the investigative methodology.

## Athena workflow

```text
CloudTrail logs in S3
        ↓
Athena external table
        ↓
SQL
        ↓
Investigation results
```

Example:

```sql
SELECT eventtime, eventname
FROM cloudtrail;
```

Event frequency:

```sql
SELECT
    eventname,
    COUNT(*) AS event_count
FROM cloudtrail
GROUP BY eventname
ORDER BY event_count DESC;
```

### Key takeaway

For smaller investigations:

```text
CloudTrail
→ PowerShell
→ jq
```

works well.

For larger AWS environments:

```text
CloudTrail in S3
→ Athena
→ SQL
```

provides a more scalable approach without needing to download all the logs locally.

Partitions can also restrict queries to relevant time periods and reduce the amount of data scanned.

---

# Windows PowerShell Cheat Sheet

| Linux-style operation | Windows PowerShell |
|---|---|
| `find . -type f` | `Get-ChildItem -Recurse -File` |
| `cat` | `Get-Content` |
| Read full JSON | `Get-Content -Raw` |
| `sort` | `Sort-Object` |
| `grep` | `Select-String` |
| `>` | `Set-Content` |
| `>>` | `Add-Content` |

The reusable CloudTrail pattern became:

```powershell
Get-ChildItem -Recurse -File -Filter *.json |
    ForEach-Object { Get-Content -Raw $_.FullName } |
    jq -cr 'JQ_QUERY' |
    Sort-Object
```

For jq queries containing string comparisons in PowerShell, escaping was required:

```powershell
jq -cr ".Records[] | select(.eventName == \`"AssumeRole\`")"
```

---

# Final Takeaways

The Defender Track reinforced several Cloud IR skills:

- CloudTrail is foundational for reconstructing AWS activity.
- Identity is central to AWS incident response.
- Timelines become much more useful when source IP, principal, event, and user agent are correlated.
- `jq` is extremely effective for quick local CloudTrail analysis.
- PowerShell can perform the same workflow even when training material assumes Linux.
- Resource policies are often as important as identity permissions when determining root cause.
- Athena provides a scalable SQL-based alternative when CloudTrail datasets become too large for local analysis.

The most useful workflow from the lab was:

```text
Collect logs
   ↓
Build timeline
   ↓
Identify suspicious API activity
   ↓
Pivot to identity
   ↓
Confirm credential misuse
   ↓
Inspect affected resources
   ↓
Identify configuration weakness
   ↓
Determine root cause
```

This is the part of the Defender Track worth retaining as a repeatable AWS incident-response methodology.
