---
type: is
id: is-01m1z08x8jehjqy5w9arvfxkxq
title: Refresh the sweep baseline from both comparable PR116 CI receipts
kind: bug
status: closed
priority: 1
version: 2
spec_path: packing/campaign/agendas/agenda-027-compatibility-and-restricted-families.md
labels: []
dependencies: []
parent_id: is-01m1ytzagmmx58w96ksbf5j3dj
created_at: 2026-09-07T22:36:56.437Z
updated_at: 2026-09-07T22:40:25.009Z
closed_at: 2026-09-07T22:40:25.007Z
close_reason: Six-sample baseline and matching development table corrected; all policy ratios unchanged. High editor63s22:37:28–22:38:31; static budget checker passes1.22s. Root owns final gates and next actual CI.
resolution: null
duplicate_of: null
---
PR116 d6 run34166034785 sweeps correctness passed58.38s but stale ratio failed versus107.05. c3 run34164869950 same four steps, runner image, cachehit, source selection and shape measured109.16s. Append BOTH to four retained readings; geometricmean97.07455, ceiling194.0 satisfies unchanged2x headroom. Preserve source/runner/cache evidence and unknown hardware/load, observedspread1.87, no speedup claim. Update gate-budgets and development table together; never copy incomingPR111 different workload null baseline. Existing point-band weakness stays think-be1s. At most5minutes high mechanical edit; no target or heavy gates.
