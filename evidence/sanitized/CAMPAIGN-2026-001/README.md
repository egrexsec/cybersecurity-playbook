# CAMPAIGN-2026-001 Sanitized Evidence

- Validation date: 2026-08-03 UTC.
- Scope: one approved Windows victim, victim-local loopback delivery, benign content only.
- Sequence: PowerShell web retrieval → local mshta execution → benign PowerShell child.
- Transfer integrity: source and staged HTA hashes matched.
- Detection correlation: DET-2026-014 followed by DET-2026-015 three seconds later.
- Completion marker: verified.
- Cleanup: first and idempotent second passes returned zero residue.

Raw event XML, active observables, environment identifiers, and private rollback details remain in approved private storage.
