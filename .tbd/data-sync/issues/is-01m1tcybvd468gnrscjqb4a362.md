---
type: is
id: is-01m1tcybvd468gnrscjqb4a362
title: The pull-request surface's 5s per-test ceiling is not stable at its own concurrency
kind: bug
status: open
priority: 1
version: 1
labels:
  - tooling
dependencies: []
created_at: 2026-09-06T03:42:10.284Z
updated_at: 2026-09-06T03:42:10.284Z
---
`fast behavioral tests` fails on a different, essentially arbitrary set of tests each run,
so the `checks` surface has never been green and cannot be made green by marking.

## Evidence

Three CI runs of `packing-validate --checks --jobs 3 --inner-jobs 1`, same branch, on
consecutive heads:

| run | tier wall | tests at or above the 5s ceiling |
| --- | ---: | --- |
| `86b883ba` first | 269.01s | output lost (killed with an unflushed pipe, D-456's shape) |
| `86b883ba` re-run | 269.01s | 1 — `test_exhaustive_connected_graph_quotient_through_five_vertices`, 5.23s |
| `8a84dca7` | 291.70s | 5 — motion-lab ×3, `test_n40_rigidity`, `test_check_declared_bounds`; **none of them the previous one** |

Every one of those tests measures at or under 2.2s on a four-core box running the same
command. The set that crosses tracks the runner's load, not the tests.

PR #87's own head `717078ca` failed this same step and merged; main's push path runs a
different command (`--skip … --jobs 2 --inner-jobs 2`), so main looks green while this
surface has never passed. The budget entry says so itself: `measured_seconds: null`,
"this tier has never run".

## Why marking cannot fix it

Tried on `8a84dca7` and reverted. Deferring the one named test moved the failure to five
others. Each marker is quick-lane coverage given up for a reason nobody measured, which is
what `test_the_slow_marker_is_declared_only_by_measured_nodes` exists to prevent, and the
process does not converge because the next slowest test is always within variance of the
line.

## The cause

`--jobs 3` runs three gate steps concurrently on four cpus, so the quick lane shares the
box with `type floor (basedpyright)` and the rest. A per-test `call` time inflates two to
three times against an uncontended measurement. The 5s ceiling and the 2s marking
threshold were both calibrated on a lane that had the box to itself — the constant's own
comment says the gap between them is "runner variance", and this is more variance than the
gap was sized for.

## Options, none of them free

1. **Give the pytest lane the box within the tier.** Schedule `fast behavioral tests`
   alone and the cheap steps around it, rather than three heavy steps at once. Keeps both
   thresholds meaningful; costs some wall.
2. **Raise the failure ceiling** to cover the measured contention, keeping the 2s marking
   threshold. Cheapest, and it weakens the guard by exactly the factor it is raised.
3. **Measure `call` time against a contention-normalised baseline** rather than a wall
   constant. Correct and the most work.

`BC-218` is the cell that owns this tier's calibration.
