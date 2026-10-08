---
type: is
id: is-01m4eqftn9s8p598th62bk0rk8
title: Calibrate portable control snapshot budget for retained rigidity metadata
kind: task
status: in_progress
priority: 2
version: 3
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4e35s7r1e65r1qmpz250h0p
hold: null
hold_until: null
created_at: 2026-10-08T21:42:40.552Z
updated_at: 2026-10-08T21:47:14.675Z
started_at: 2026-10-08T21:43:07.260Z
---
The cleanup pre-push run found 201,971,305 copied worker bytes against a 192 MiB cap (201,326,592), with unchanged PDF pruning. The prior gap-export revision had only45,663 bytes headroom; most growth is564,800 bytes of structured rigidity source/date metadata in composite-figure.json, consumed by validate_schemas. Independently review the measured budget disposition, preserve scientific inputs and cap assertions, then validate the three affected controls.

## Notes

Independent read-only audit reproduced201,971,305 bytes across6,757 copied paths; retained composite rigidity source/date metadata contributes564,800 bytes of growth and validate_schemas consumes it. Calibrated the production cap from192 to200MiB (7.39MiB measured headroom; three-worker ceiling600MiB) with a dated rationale; preserved pruning, dependency rescue, copying, timeouts and oversize refusal. Four existing checks passed:2 clone-free/refusal tests in1.62s and2 shared real-copy/input-preservation tests in28.05s. Independent review found no issues. Maintained audit and exact logs are retained outside disposable scratch; settled full gate still pending the latest design refinements.
