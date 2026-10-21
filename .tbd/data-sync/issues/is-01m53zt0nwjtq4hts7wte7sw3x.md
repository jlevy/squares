---
type: is
id: is-01m53zt0nwjtq4hts7wte7sw3x
title: "T-193 RE-1: name the packing each of nine exact forms solves, with measured identities (#658 A8)"
kind: task
status: open
priority: 2
version: 4
delegate: null
labels:
  - result-import
dependencies: []
parent_id: is-01m51e5r3sg4h1wcrh7c826v7b
hold: null
hold_until: null
created_at: 2026-10-17T03:52:06.075Z
updated_at: 2026-10-19T21:44:22.639Z
started_at: 2026-10-17T03:52:27.706Z
---
The T-193 stage 4 review's RE-1 (major), found in docs/project/reviews/review-2026-10-16-evand-exact-sides-639.md and deferred by PR #658 (review A8 asked for an owning bead before merge).

At 88, 126, 175, 199, 204, 232, 266, 292 and 301, T-193's `regularizations` items name PingYou Ltd's refinement (T-174) or Polkovskyi's (T-186) as the packing each exact form solves (`of`), but the review measured each form to be the case's own house there (T-127, T-139, T-158, T-162, T-119, T-146, T-098), to within 4.5e-4 at every centre. T-193's claim and notes already say so; the items themselves are uncorrected.

## Validation
- Claim: each of the nine items names, as `of`, the register entry whose packing the form re-solves, with `identity.basis: measured` and the review as `measured_in`.
- Run: rewrite the nine items in packing/frontier/results.yaml from the review's pose-by-pose measurement (its programs in packing/resources/web/evand-exact-cur-2026-10-16/review/review-2026-10-16/), then `check_results`, `render_results --check` and the house-adoption tests; under the house rule `select_houses` credits the packing through `of`, so `select_houses --all` shows the new credit at each count.
- Waits on: the owner's Q2 in that review (whether a square turned at its centre is the same packing).
- Cost: under 0.1 CPU-h; records only.

## Notes

2026-10-19 lane-658 (#658 review D4, after review B1's fix): returned to open with no delegate. Nothing can be done until the owner answers Q2; the claim under user-eb-addr-658 (a lane that has ended) would have made the next tbd start skip. CORRECTIONS_OWED in select_houses blocks adoption at the nine counts meanwhile.
