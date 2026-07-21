# EVTX Analysis Workflow

## Intended flow
1. export EVTX from approved collection profile
2. verify hashes
3. process with Hayabusa
4. process with Chainsaw
5. normalize outputs
6. merge into unified case timeline
7. perform analyst review

## Current live status
- Hayabusa: not present on DFIR during assessment
- Chainsaw: unconfirmed during assessment
- workflow and repo structure: implemented
- validated offline execution: not yet complete

## Required stored outputs
- command transcript
- tool versions
- input hashes
- output paths
- normalized result JSON/CSV
