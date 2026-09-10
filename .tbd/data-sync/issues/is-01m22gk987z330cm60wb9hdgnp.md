---
type: is
id: is-01m22gk987z330cm60wb9hdgnp
title: "X-024 slice A3: the threshold loop at 383/100 from the accepted 191/50 site and atom set"
kind: task
status: closed
priority: 1
version: 3
labels: []
dependencies: []
created_at: 2026-09-09T07:19:56.934Z
updated_at: 2026-09-09T15:08:24.694Z
closed_at: 2026-09-09T15:08:24.694Z
close_reason: "A3 measured, no bound: the covering LP on the accepted 191/50 columns is 11.0179 at 383/100 and exactly eleven at 153/40, one two-of-three atom round moves it by 3e-9, and both plateau duals are refused by the plateau reader at depth about 1.12 and 1.10, so neither caps the method. Site separation shrinks the deep region slowly. The open question is carried by think-7rqw (slice A6). Lane report: packing/campaign/series/series-000-smoke-and-calibration/results/agenda-033/lane-a3-threshold-loop-at-383-100.md"
resolution: null
duplicate_of: null
---
H-147, second half. Rows-only loop at L = 383/100, B = 9977/10000, 181 directions, warm-started HiGHS; then one atom-separation round if the value refills to eleven. A rows-complete value below eleven freezes and goes through the gate; a plateau is read against its dual.
