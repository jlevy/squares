---
type: is
id: is-01m13h894wrjjmbbx7cm35e500
title: sqpack.field mutates the global decimal context, leaking precision across a process
kind: bug
status: open
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01m12zjr144a4kg6rnv1t0pm6n
created_at: 2026-08-28T06:34:57.558Z
updated_at: 2026-08-28T06:35:21.730Z
---
src/sqpack/field.py:500 in FieldContext.decimal() sets decimal.getcontext().prec = digits + 20. That is the PROCESS-GLOBAL decimal context, not a local one, and it is never restored, so every Decimal computation afterwards in the same process runs at the raised precision. With the default digits=100 the context goes to 120 and stays there.

Observed consequence: tests/test_verified_upper_bound_contract.py compares a gap rendered into the frontier records at Python's default 28 digits. Run alone it passes; run in the full fast suite after anything that refines a field enclosure, Decimal renders 0.196616925283891613096163316624010302329936671 instead of 0.1966169252838916130961633166 for n=68, and the test calls the record stale. The record was never stale; the ambient precision had moved. Reproduced deterministically with -p no:randomly, and demonstrated directly by setting prec to 120 by hand.

Worked around in that test by pinning a local context at 28 with a comment, but the leak itself is untouched and the blast radius is wider than one test: any code that formats or compares Decimals after a field refinement silently changes behaviour, and nothing announces it.

DONE WHEN: FieldContext.decimal(), and any sibling doing the same, raises precision inside a decimal.localcontext() block so the caller's context is restored on exit, and a test asserts that calling it leaves decimal.getcontext().prec unchanged.
