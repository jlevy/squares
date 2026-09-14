---
type: is
id: is-01m2b883mnsa3g9ap94gy5aj0q
title: Retain observed worker topology in BC329 calibration profiles
kind: task
status: in_progress
priority: 1
version: 11
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
delegate: Sol xhigh implementation; source-distinct review
labels:
  - n11
  - calibration
  - tooling
dependencies:
  - type: blocks
    target: is-01m2b884n0ms50xp93q6aaps1g
  - type: blocks
    target: is-01m2appdgg1p32xwgxptcqqb2x
  - type: blocks
    target: is-01m2cv85q2ajjgsnx7076ta8cp
parent_id: is-01m2app5e71qnp9z5vfp9vppbp
hold: paused
hold_until: null
created_at: 2026-09-12T16:47:12.009Z
updated_at: 2026-09-14T02:28:52.550Z
---
Run-sheet review F-1. Before any positive full-shape profile, extend the maintained fixed-core-packet-calibration/v1 measurement contract to distinguish configured route workers from observed execution. Retain the supervised coordinator PID and per-sample PID/PPID/PGID/phase data, or an equivalent route-scoped worker lifecycle record; derive and validate observed child count and maximum simultaneous children for raw and normalized-exact phases. Refuse metrics admission if the parallel phase has no observation capable of checking worker execution. Keep RSS explicitly a sampled process-group sum with missed-peak/shared-page limits. Add focused mutation and lifecycle tests, source-distinct review, and do not run a profile or BC329.

## Notes

Topology producer lifetime guard integrated in fc3e314d, paired with coordinator temporal validation. Prior exact-head reviewer found coherent future task times accepted; focused suite passed 121 and static gates clean. Independent exact-head coordinator/topology rereview active; reader review additionally found task/phase/lifetime and self-parent contradictions that are being repaired in source-distinct consumer. No positive profile or BC329 ran.

Paused: 2026-09-14 owner hold (think-zwlf): BC329's prospective gain is about 0.000274 over T-026 s(11) >= 3.8264474, and heavy computer-assisted work for very small improvements is paused while the program re-strategizes toward significant n=11 improvements or a much simpler proof. The runner, reader, verifier and run sheet land as retained, unexecuted machinery with PR #156 (think-j007). Resume only by an explicit owner decision.
