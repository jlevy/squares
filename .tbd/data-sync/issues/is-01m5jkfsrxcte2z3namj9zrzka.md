---
type: is
id: is-01m5jkfsrxcte2z3namj9zrzka
title: "Evan Daniel replay entries: the maintained evand adapter transcribes the source's corners and parse; add producer-code to read, fix 'copies none' statements (#728 review RF-1)"
kind: task
status: open
priority: 3
version: 2
labels:
  - records
dependencies: []
created_at: 2026-10-22T20:05:24.893Z
updated_at: 2026-10-23T02:53:19.960Z
---
From the stage 4 review of #728 (c-review-728-math, scratchpad/review-728/review-2026-10-22-daniel-728.md, RF-1, minor).

The maintained evand adapter's `Pose.corners` and its comment/blank-line filter are transcriptions of the source's `verify_cert2.corners` and checker parse (evand/square-packing search/exact/). The record says the adapter "copies none of their code", and the earlier evand replay evidence entries' `read` lists omit `producer-code`. The source's checkers are standalone and share no code with this repository's deciders, so this is not the Couzo RF-1 case (shared sqpack.verify), but the independence statements are inaccurate.

#731 (T-230, #728) corrects its own entry. To do here: a records pass over every earlier evand replay entry (n155, n183, n229, n270, n308, n343 and any other evand-cert adapter consumer; `rg -n "evand-cert|evand_cert" packing/`): add `producer-code` to `read`, name the two transcribed expressions, and correct the adapter's module statement and the verifier-registry note. No verdict or rung changes are expected; confirm per entry.
blocked_on: none

## Notes

2026-10-23 (c-lane-728-import, review A2 of #731): T-230's own maintained replay entry, E-evand-728-n303-exact-feasibility, is settled in #731 at 868925d6b: relationship_to_generator shared-components, the two transcribed expressions (the adapter's line filter, Pose.corners from verify_cert2.py's corners) in shared_components and in independence.shares, overlaps_producer.separate_code false, the note citing epistemics.md ("a transcription shares those definitions"). No rung moved: T-230 stays confirmed, independently re-implemented, on the clean-room E-evand-728-n303-review-exact-feasibility. V-evand-exact-certificates gained a second version (56340bd7..., docstring only). The earlier evand replay entries remain for this bead; the same reading (shared-components, not only producer-code in read) is the precedent review A set.
