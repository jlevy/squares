---
type: is
id: is-01m1b297gm8m0cpghtxaz8f9hy
title: "Lane A0: generalize the unavoidable-set certifier into a resource-system instrument"
kind: feature
status: closed
priority: 1
version: 6
spec_path: packing/campaign/explorations/X-010-two-lanes-two-ladders.md
labels:
  - x-010
  - lane-a
dependencies:
  - type: blocks
    target: is-01m1b29qrvdzvmjb2n22n5826h
  - type: blocks
    target: is-01m1b29r4pe1vvj5vzp2kqpsxt
  - type: blocks
    target: is-01m1b297ydh4ahazqwk4mx6hqq
created_at: 2026-08-31T04:47:15.476Z
updated_at: 2026-08-31T05:56:12.953Z
closed_at: 2026-08-31T05:56:12.943Z
close_reason: "BC-093 discharged by session-050 phase 1: sqpack/cover.py is the general core, both Stromquist modules reduced to callers (-403 lines), exp-016/exp-017 replays byte-stable (exit 0, only run-dependent elapsed_seconds differs), 8 tests pin the core on a plain-rational scalar, typed refusals for weighted-point/segment/threshold-charge/moving-family, FieldElement seam recorded in the docstring. ruff/basedpyright clean."
resolution: null
duplicate_of: null
---
cases/stromquist/repaired_cover.py certifies one figure over a bespoke Q(sqrt 5) embedding in 1868 lines; printed_cover.py refuses the printed set. Extract the reusable core: a declared resource system (points, weighted points, segments with length thresholds, threshold charges, moving families) over sqpack.field scalars or rational intervals, a box family at a declared container side, and a replayable cover certificate. Exit: the exp-016/exp-017 Stromquist pair replayed through the general instrument -- printed refuses, repaired certifies, byte-stable -- with the bespoke module reduced to a caller. Should consume sqpack.field or record why not (the Q5 seam is where a certifier defect would live). Unlocks Bentz m=4, the Green sizes, think-at4f, H-033. X-010 Lane A rung 0.

## Notes

agenda-010 BC-093 (block 1 first).
