---
type: is
id: is-01m31gnrvrkg5ec6ccnh6nmeja
title: H-226 regime specifies 25 red points, contradicting its own claim and Bentz
kind: bug
status: closed
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m31gn7263sfhfbq8xfabkh3p
created_at: 2026-09-21T08:17:45.838Z
updated_at: 2026-10-06T08:47:30.118Z
closed_at: 2026-10-06T08:47:30.117Z
close_reason: "Done: packing/campaign/hypotheses/H-226-n21-one-spare-wall-charge-lemma.md on origin/main now places 5 red points in rows 2 and 4 and 4 in rows 1, 3, 5 (red 22, blue 23), with blue on the integers in rows 2 and 4; H-226 is refuted in the ledger."
resolution: null
duplicate_of: null
---
PR 204 review finding F2 (Medium), but urgent: BC-362 is ready, so the enumeration instrument is built from this regime next. packing/campaign/hypotheses/H-226-n21-one-spare-wall-charge-lemma.md gives red as {0.5..4.5 step 1} x {0.9,1.7,2.5,3.3,4.1} = 25 points, against its own claim of 'the 22 red and 23 blue points'. PDF page 6 gives the union of both colours as 45 points with only red rows r2 and r4 carrying 5, so red = 4+5+4+5+4 = 22 and blue = 23. 'blue set on the interleaved half-integers' is also wrong: blue sits on the integers in rows 2 and 4. Built to this regime the tool enumerates 25 red points, loses the (1,2) spare structure defining the case, and records a verdict against a regime that is not Bentz's.
