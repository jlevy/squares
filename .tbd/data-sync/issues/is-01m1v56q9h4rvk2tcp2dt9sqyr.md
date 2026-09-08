---
type: is
id: is-01m1v56q9h4rvk2tcp2dt9sqyr
title: Arm the gate-budget drift rule against run-to-run spread, not a single sample
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-09-06T10:46:09.964Z
updated_at: 2026-09-06T10:46:09.964Z
---
gate-budgets.yaml compares against one recorded measured_seconds with a 1.5x drift rule and a 0.6x stale rule. Measured run-to-run spread on the hosted runners is about 34% (chunk census 81.18s vs 108.91s on identical code; validate 112s vs 133s), so a 1.5x rule sits close to the noise floor: it will fire on quiet regressions and stay silent on real ones. Record a band over repeated samples rather than a point, or move the comparison to cpu-seconds the way devtools/cpu_durations.py does per test. See D-472.
