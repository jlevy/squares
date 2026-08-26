---
type: is
id: is-01m0ypc5cd4z6ktb1vejj1td3n
title: "W7: deterministic chunk partitions and contact-assembly grammar"
kind: feature
status: in_progress
priority: 1
version: 13
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-26-overnight-constructive-enumeration.md
labels: []
dependencies: []
created_at: 2026-08-26T09:28:15.500Z
updated_at: 2026-08-26T18:53:25.183Z
---
BC-019. The bounded lattice splitter is implemented: it enumerates contiguous bars, filled rectangles, and corner Ls, minimizes F then C, emits canonical certificates, and types search limits. Calibration result: all 64 grids but only 2/36 non-grid cases fit the narrow six-chunk/two-free budget; eight more need 7-12 chunks, 23 have no partition in this universe, and three hit the 10,000-state cap. Next: version a same-angle contact-chain/tree/patch grammar with LP-resolved slide degrees and a non-vacuous complexity cost. The inspected n=1..100 corpus remains calibration-only; no H-044 verdict.

## Notes

2026-08-26 PR 45 handoff: branch head 8ff368f is pushed. Full review verdict is revise. P1 follow-ups are think-oo1p (partition free-count short circuit and dependent 3/2/23/8 regeneration), think-givb (Kingbird reuse basis), and think-4axm (durable record reconciliation after corrected outputs). P2 follow-ups are think-9jny (mixed angle-class local solver) and think-rov3 (co-committed hash policy). Session 017 and its ledger row are terminal. Replacement CI run 33002078000 is active. Under BC-019, start with think-oo1p; keep the 1-100 corpus calibration-only and the 11,013-orbit atlas abstract-only.
