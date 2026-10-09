---
type: is
id: is-01m4eqftn9s8p598th62bk0rk8
title: Calibrate portable control snapshot budget for retained rigidity metadata
kind: task
status: closed
priority: 2
version: 5
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4e35s7r1e65r1qmpz250h0p
hold: null
hold_until: null
created_at: 2026-10-08T21:42:40.552Z
updated_at: 2026-10-09T13:44:10.835Z
started_at: 2026-10-08T21:43:07.260Z
closed_at: 2026-10-09T13:44:10.835Z
close_reason: Implemented, independently reviewed and qualified for PR474 source 6ccbbf000f0c9b48f2985c07c9893f98fe73ba92 against main 6a0499ba4; combined tree c65da41410e89a8dedffe93d3c1e153adb05096d. Local named push 65/65 and hosted 93 fast + 13 actual deferred (106) plus Pages passed; final readiness receipts recorded.
resolution: null
duplicate_of: null
---
The cleanup pre-push run found 201,971,305 copied worker bytes against a 192 MiB cap (201,326,592), with unchanged PDF pruning. The prior gap-export revision had only 45,663 bytes headroom; most growth is 564,800 bytes of structured rigidity source/date metadata in composite-figure.json, consumed by validate_schemas. Independently review the measured budget disposition, preserve scientific inputs and cap assertions, then validate the three affected controls.

## Notes

Independent read-only audit reproduced 201,971,305 bytes across 6,757 copied paths. Required rigidity metadata accounts for 564,800 bytes of growth. Calibrated the production cap from 192 to 200 MiB (7.39 MiB measured headroom; three-worker ceiling 600 MiB), preserving pruning, dependency rescue, copying, timeouts and oversize refusal. Four existing checks passed: two clone-free/refusal checks in 1.62s and two real-copy/input-preservation checks in 28.05s. Independent review is clear. The maintained audit and exact logs are retained outside disposable scratch; final pre-push and hosted gates remain under think-142l.
