---
type: is
id: is-01m1v56q9h4rvk2tcp2dt9sqyr
title: Arm the gate-budget drift rule against run-to-run spread, not a single sample
kind: task
status: open
priority: 2
version: 2
labels: []
dependencies: []
created_at: 2026-09-06T10:46:09.964Z
updated_at: 2026-09-08T23:14:38.901Z
---
gate-budgets.yaml compares against one recorded measured_seconds with a 1.5x drift rule and a 0.6x stale rule. Measured run-to-run spread on the hosted runners is about 34% (chunk census 81.18s vs 108.91s on identical code; validate 112s vs 133s), so a 1.5x rule sits close to the noise floor: it will fire on quiet regressions and stay silent on real ones. Record a band over repeated samples rather than a point, or move the comparison to cpu-seconds the way devtools/cpu_durations.py does per test. See D-472.

## Notes

Additional evidence from font PR #135 on 2026-09-08: consecutive reference-shape suite runs at dfa0a422 and a10569d1 selected the same 4,283 tests with unchanged workflow, dependency lock and selection code. Gate walls were 158.64s (run 34285770932/job 102260892830, Ubuntu image 20260831.293.1) and 88.84s (run 34288782986/job 102270405743, image 20260907.300.1). All tests passed; the second job failed solely below 0.6 of the old 162.62s single-point baseline. think-uwow refreshes the record to their 118.72s geometric mean and tightens ceiling to 237s without changing policy. The 1.79x hosted spread is not evidence of a code speedup. Broader band/runner-aware policy work remains here, outside the typography release.
