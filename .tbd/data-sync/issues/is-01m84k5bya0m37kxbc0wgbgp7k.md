---
type: is
id: is-01m84k5bya0m37kxbc0wgbgp7k
title: "Intake: verify Özden's 264-square packing (#1099)"
kind: task
status: in_progress
priority: 2
version: 7
delegate: codex-intake-1099
labels:
  - intake
  - validation
dependencies: []
hold: null
hold_until: null
created_at: 2026-11-23T16:17:26.473Z
updated_at: 2026-11-23T18:59:25.866Z
started_at: 2026-11-23T16:17:39.786Z
---
Review https://github.com/jlevy/squares/issues/1099 and pinned rational-corners witness kenaznia-doga/s264-upper-bound-1677216830@72c4d195c85b6099002ad6c675b27df40fdaceac. Replay exact and independent verifiers, review provenance and compare with the T-308 house and GeiserX #1037 before disposition and potential adoption. Reviewed alongside the 23 November intake.

## Notes

23 November intake. Retained the pinned 721,390-byte rational-corners Witness/v2, issue JSON and published digest under external evidence drawing-audit-20261122/n264-1099-triage. Both maintained exact rational GMP paths verified all 264 unit squares and 34,716 pairs at side 16.77216830504054639626340160… and rejected duplicate-square and outside-wall controls. Each exact output and the memory-guard receipt are retained alongside it. Side is 0.00163929296145 smaller than published T-308 and 0.000674847636987 smaller than the retained but not yet adopted GeiserX #1037 report. The disclosed Kaggle leaderboard number with no coordinates is 0.00187977729055 smaller. Scope is finite feasible upper bound. Pending stage-3 source packet, report-order disposition, and house adoption with regularization.

Independent strongest-tier review completed. Checker that shares no producer or project geometry verified 264 unit squares, 1,056 wall inequalities and all 34,716 pairs, with exact near-distance checks for 578 pairs within 1e-8 and eight analytic controls. Minimum gap is positive, about 2.876e-13 between squares 1 and 6. One low finding: the issue describes centre/half-angle while the canonical file holds rational corners. Packaged source custody and stage-3 checks passed in external branch codex/intake-n264-ozden-20261123. Native formal handoff and Stage 5 adoption with drawing regularization remain active.

Full native positives and two gross controls passed on both GMP routes, and the independent review accepted a finite upper bound. Additional sharp suite reached its declared wall cap, recorded as such. Stage 5 adopted T-343 locally and exercised all four strong generator runs. Exact same-side grid 1° was selected; 5° had identical witness bytes. New default improves 697/723→707/741 full-side contacts versus T-308, with near-axis 0, uneven 28 and light 4→6. Drawing state and flip check passed. Data checkpoint rebased onto released main as fb20f38488ba and pin 556853f1cf; final derived checks and paper disposition underway.


## Draft follow-up for #1099

Thank you for submitting the exact witness. The registry now records **T-343 at V3/C3**, with **s(264) ≤ 16.772168305041** when rounded upwards to 12 decimal places. This improves the preceding verified house, T-308, by about 0.00164. The record credits Tomáš Kodaj and JoeGun for the seed packing, you for this refinement, and Evan Daniel for the optimizer. [Published case and drawing](https://squaremath.org/cases/264.html) · [Result T-343](https://squaremath.org/result/t-343.html).

The project's maintained exact replay used `packing-witness verify` and `devtools.check_rational_witness_independent` with rational arithmetic. Both accepted the full witness and rejected the duplicate-square and outside-wall controls. A separately written exact checker also verified all 264 squares and 34,716 pairs directly from the pinned rational corners. The default drawing regularizes the packing at the same exact side. [Retained certificate and replays](https://github.com/jlevy/squares/tree/main/packing/resources/web/ozden-s264-upper-bound-2026-11-23).

This completes your registration request. If coordinates for the quoted 16.770288527750 Kaggle result become public, could you link them here? They would help with a future comparison.

2026-11-23 final hosted retry: #1102 at 9bb725c47b1ada2d50638a7ceb34a29a229f7107. The previously failing results-render and custody tests both pass locally. The maintained custody regenerated 78 houses, 268 inputs and 106 refused and restored mutations, rebinding the corrected report.json; release pin checked at bc26be0fe1dd. The independent scoped review is posted. Hosted gates, deployment verification, author close and S3 News remain in order.
