# Identity investigations

**Capability maturity: Planned**

This domain will cover authentication, credential abuse, lateral movement, directory changes, and privilege escalation. No identity investigation is represented as implemented or validated yet.

## Planned cases

| Case | Scope | Status |
|---|---|---|
| `MAY-IR-003 credential abuse/lateral movement` | Correlation across approved Windows systems | **Planned** |
| `MAY-IR-004 AD privilege escalation` | Directory privilege analysis with identity and endpoint correlation | **Planned** |

## Evidence expectations

Future cases should correlate authoritative identity records with endpoint and network telemetry, preserve account and host context, distinguish successful from failed activity, and document benign explanations considered. Credentials, tokens, directory exports, and raw authentication logs remain private; public artifacts must be sanitized.
