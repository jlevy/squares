---
type: is
id: is-01m5rr1xq0hjnz6409nrc5kd8h
title: "Import #804: Hyukdong Kim's exact minimal polynomials of the record sides at 88, 126, 172, 199, 263"
kind: task
status: in_progress
priority: 2
version: 21
delegate: bold-ritchie-l14
labels:
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
child_order_hints:
  - is-01m5s72s7x05kxkyzxjkfqf2wh
  - is-01m5sas1vt59d996xv22h14rr7
hold: null
hold_until: null
created_at: 2026-10-25T05:20:39.648Z
updated_at: 2026-11-01T16:48:33.303Z
started_at: 2026-10-25T05:21:00.185Z
---
New 2026-10-25 issue https://github.com/jlevy/squares/issues/804 (HyukdongKim, 01:57:25Z): the record side at each of 88, 126, 172, 199 and 263 is a root of a stated irreducible polynomial (degrees 7, 2, 24, 16, 17; 126 = 15/2 + 3 sqrt 2), the register having minimal_polynomial: null there; exact_forms.json. Claude-assisted. Stage 1 triage read-only first: which houses the polynomials describe today (the record has moved since 2ec489d1e at some counts?), how to verify (exact KKT/rigidity system, PSLQ is not a proof), and the register action (new exact-value entries, or evidence on the houses).

## Notes

2026-11-01 bold-ritchie-l14 (PR #868, ccd265cac): squares-exact-forms.zip's seven files kept byte-identical under hyukdongkim-exact-forms-2026-10-25/source/ from the public copy f480441e (zip = issue's c770f9c3...4ee7); sources.json records the public copy and CC0; #804 ask marked done. Close after #868 merges.
