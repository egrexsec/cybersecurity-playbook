# Splunk Alert to Case

## Payload contract
Use `schemas/alert-intake.schema.json`.

Required fields:
- `alert_name`
- `rule_id`
- `severity`
- `host`
- `user`
- `process`
- `parent_process`
- `command_line`
- `event_time`
- `technique_id`
- `event_id`
- `splunk_index`
- `splunk_sourcetype`
- `search_reference`

## Flow
1. webhook receives structured payload
2. authenticate source
3. validate schema
4. derive deduplication key: `rule_id + host + user + time-window`
5. create/update case
6. run `playbook ir enrich <case-id>`
7. select forensic profile
8. run `playbook ir collect <case-id>`
9. run `playbook ir hunt <case-id>`
10. generate timeline and report
11. notify analyst

## Current implementation note
This branch implements the repository-side controller and workflow export; Splunk-side saved search / alert object creation remains a manual integration step.
