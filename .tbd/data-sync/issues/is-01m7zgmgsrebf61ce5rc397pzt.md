---
type: is
id: is-01m7zgmgsrebf61ce5rc397pzt
title: "Review #1052 bounded-motion minimum-centre claim for the 37-turn variant"
kind: task
status: closed
priority: 1
version: 4
delegate: codex-intake-1119-01a1fb
labels:
  - validation
dependencies: []
parent_id: is-01m7z5m459vq8zrvf2ek5z3v0v
hold: null
hold_until: null
created_at: 2026-11-21T16:57:05.079Z
updated_at: 2026-11-22T20:27:15.307Z
started_at: 2026-11-21T17:45:36.126Z
closed_at: 2026-11-22T20:27:15.304Z
close_reason: "Exact bounded minimum nine merged in #1081 (9ef2fa9f), verified live by Certificate page run 45064698435 and reported at https://github.com/jlevy/squares/issues/1052#issuecomment-7085234329. The case drawing comparison remains on think-rbyl."
resolution: null
duplicate_of: null
---
Review the pinned author proof independently. Match both square-43 alternatives, the 2e-11 motion bound and disjunctions for all separating axes, and replay all 34 local Z3 infeasibility checks plus completeness of the 17-group hitting-set argument. This is a restricted claim for fixed alignment/snap choices. Use independent code and retained controls. Neither the original T-336 house nor its rung depends on this result.

## Notes

21 November bounded progress. Exhaustive maintained set cover of the 17 submitted fixed-center groups has minimum cardinality 9, 1,581 minimizers and 10,991 visited nodes. Two small controls passed and the 37-turn witness's moved centers hit every group. This is conditional on each group's local infeasibility premise. Separately restored square 43's exact original orientation in the accepted 37-turn witness, leaving the same nine changed centers and 36 changed directions. Both maintained routes accepted that exact 36-turn positive, under the original side and 2e-11 coordinate cap. Nine centers therefore suffice for both alternatives. Still required before asserting minimality: the independent 34 local geometric exclusions with exact solver inputs, matched controls, sound pair-pruning and reviewed arithmetic. Z3 is absent from the pinned local environment.
