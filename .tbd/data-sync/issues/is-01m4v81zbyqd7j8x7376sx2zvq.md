---
type: is
id: is-01m4v81zbyqd7j8x7376sx2zvq
title: Replay sq17-lean's full build (4,951 modules, three archives) on a large machine, for T-154's V3/C3
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m4v5ne8b1dq1gyybx5mj689d
created_at: 2026-10-13T18:23:05.598Z
updated_at: 2026-10-13T18:23:05.598Z
---
The source's own command (README at e6ee548): unpack the three v1.0.0 archives (1,962,867,415 B, 6,986,311,712 B unpacked), lake exe cache get, python3 scripts/reproduce.py build --jobs 40 --proof-jobs 8, accept only REPRODUCTION_ACCEPTED Sq17Lean.Square17Optimality with the axiom set of verification/Square17Optimality.log (3 standard + 13,343 native_decide, no sorryAx). Needs Lean 4.34.1 with leanc, the Mathlib v4.34.1 cache and tens of GB of disk and memory; this host (4 cores, 15 GB RAM, 18 GB free disk) is too small. The source publishes no CPU or wall time, so the price is to be measured. Waits on an owner budget. Review: docs/project/reviews/review-2026-10-13-fitzharding-n17-lean.md, replay section.
