---
type: is
id: is-01m28n81fbr1gtza361f1h8yg9
title: Track what the build and the runs cost, so a slow algorithm says so
kind: task
status: closed
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-09-packing-strategies-as-a-shared-language.md
labels: []
dependencies: []
created_at: 2026-09-11T16:36:37.982Z
updated_at: 2026-09-11T16:36:49.800Z
closed_at: 2026-09-11T16:36:49.799Z
close_reason: "Built and measured in 80092bc9: per-stage build timings recorded and printed, a trajectory-cost check with a stated ceiling in the gate, and ms_per_frame in the capture receipt."
resolution: null
duplicate_of: null
---
Built in 80092bc9, recorded here so it is findable.

Three places now report their own cost:

BUILD. build_candidate.Stopwatch records per-stage wall time into transition-stats.json under build_seconds and prints it. Measured: 13.9 s in all -- 7.2 s matching the pairs (the Hungarian and the crossing repair), 3.7 s measuring them, 2.9 s reading the witnesses and renderings. The crossing repair alone is 22 ms at n = 323.

PAGE. check_workbench builds a trajectory at n = 11, 100 and 324 under both physical styles, prints what each cost, and fails over TRAJECTORY_MS_CEILING (400 ms) and TRAJECTORY_BYTE_CEILING (4 MB). Measured at n = 324: 29 ms and 1.3 MB. The ceilings are about thirteen times the time and three times the memory, loose on purpose -- wall clock on a shared machine, and a flaky performance gate is worse than none. What it catches is the shape of a regression: an algorithm going quadratic, or the broad-phase grid being dropped.

CAPTURE. The video receipt carries ms_per_frame per step and in summary. Measured: 44 ms a frame mean, worst 49 at n = 11, over a 340-frame capture.

Left open deliberately: none of these is recorded as a BUDGET that drifts, the way devtools/gate-budgets.yaml does for the validation tiers. If the numbers start moving, the next step is to put the build's stage times there too.
