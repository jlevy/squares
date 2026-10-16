---
type: is
id: is-01m51jr81g6c5pgtsqrvtk5ch0
title: "Review: Greff's mixed covers for s(76) = 9 (T-184, #594) and s(95) = 10 (T-191, #610), stage 4 review lane"
kind: task
status: in_progress
priority: 1
version: 2
delegate: user-eb-review-76-95
labels:
  - validation
dependencies: []
parent_id: is-01m51hyxstsa9ptekd2ss26ksn
hold: null
hold_until: null
created_at: 2026-10-16T05:25:27.727Z
updated_at: 2026-10-16T05:25:32.352Z
started_at: 2026-10-16T05:25:32.352Z
---
Stage 4 review lane (W2) for T-184 (#594, Benjamin Greff, s(76) = 9) and T-191 (#610, s(95) = 10), the k = 9 and k = 10 cases of the k^2 - 5 series by mixed covers in Evan Daniel's format, registered at V0/C0. Their next_rung asks for "a review that reads the cover, the two checkers' composite over the D4 region and the wall segments". Model: docs/project/reviews/review-2026-10-02-wand125-s59-s77-mixed-covers.md (T-066's review). Deliverable: docs/project/reviews/review-2026-10-16-greff-k2m5-mixed-covers-76-95.md (or similar) on its own branch and draft PR; it moves no rung.

## Validation
- Claim: the lower halves s(76) >= 9 and s(95) >= 10 by the retained mixed covers (packets bengreff-s76-certificate-2026-10-14, bengreff-s95-certificate-2026-10-15), checked by zmx2 (D4 sweep) and zm_mixed.py.
- Run: read the covers and both checkers; reproduce samples or full sweeps as priced; mutated-input controls.
- Cost: estimate unknown until read; the reviewer prices before running anything above 1 CPU-h and stays under 4 CPU-h tonight.
- Budget status: runnable within the cap for samples.
- Depends on: nothing on main; the records slice think-ccjt runs in parallel.
- Done when: the review document is pushed with its PR, findings graded, verdict per entry.
- Machine note: one process, nice; the host is shared with two regularization lanes.
