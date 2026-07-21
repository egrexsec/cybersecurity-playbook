# Detection From Investigation

## Flow
1. review confirmed observations
2. identify stable fields/behaviors
3. review existing rule coverage
4. create or improve Sigma rule
5. add positive fixture
6. add modified-variant fixture
7. add negative fixtures
8. validate rule
9. convert to Splunk
10. test historical telemetry
11. perform live replay if approved
12. document false-positive gaps and known constraints

## Anti-overfitting rules
Do not key only on:
- exact Atomic command text
- exact temporary filenames
- exact task/service names
- victim hostname
- lab-only IPs
- test usernames
