---
type: is
id: is-01m5r7y7jhn1ph707k211nv2pz
title: Adopt T-242 at 268 (H2 of think-hx0e), on or after 2026-10-26T00:00Z, and regularize it
kind: task
status: in_progress
priority: 2
version: 6
delegate: w-pr807-1026
labels:
  - result-import
  - validation
  - regularization
  - packing
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
child_order_hints:
  - is-01m5rq9t9emczj9skdj275jen7
hold: null
hold_until: null
created_at: 2026-10-25T00:39:01.456Z
updated_at: 2026-10-26T00:42:30.080Z
started_at: 2026-10-25T04:15:45.960Z
---
H2 of think-hx0e: adopt T-242 (Evan Daniel's s268_lightning.cert at evand/square-packing@8a8879a, 16.874361715869345824484822296466, 4.48e-12 below T-240) at 268 as the house, under the house rule, and regularize the new house with both strong generators in the same pull request.

Why a second pull request: #794 (think-bk9r) adopts T-240 at 268 and 303 in the pass of 2026-10-25, and the day archive (house-adoption-prior-state-YYYY-MM-DD) keeps one prior state per count per day. H1 (think-hx0e, branch claude/intake-2026-10-24-t241-t242-review) maps T-242 to V3/C3, adopts it at 304 in the pass of 2026-10-25 and stages 268 in select_houses.PENDING_ADOPTION as "next pull request" with this bead. This pull request takes 268 off that list, dated 2026-10-26, and merges on or after 2026-10-26T00:00Z; the coordinator schedules it.

House credit at 268 follows the placement adopted: Daniel after Lavrentev (review of 24 October, docs/project/reviews/review-2026-10-24-couzo-evand-n268-n304.md; T-240's review RF-6). Follow packing/campaign/result-import.md "Adopt a House, Then Regularize It" as #794 and H1 do: upper_bound_houses (T-242's packet source, ADOPTED[268], LATER_PASSES['2026-10-26']), adopt_houses (CREDITS[268], RESULTS['T-242'] prose already written by H1), build_known_best_atlas --update, regularize_axis_components --update-atlas --n 268, default_drawings --update, both strong generators, selection, feeds (custody, screen, censuses, citations, rigidity), stamp_landed, release_pin. #794's regularizer already found a KKT view at exactly T-242's side at 268 (cases/regularized_drawings/think-bk9r-2026-10-24, think-20oj).

## Validation
- Claim: s(268) <= 8437180857934672912242411148233/(5*10^29), T-242, V3/C3 after the 24 October review; maintained replay E-evand-kaggle-descents-exact-feasibility, review checker E-evand-kaggle-descents-review-exact-feasibility.
- Run: adopt_houses for 268; Evan Daniel's regularizer and grid-slack (0.5, 1, 5 degrees) on the new witness; the selection.
- Cost: about 15-30 CPU-minutes, from #794's runs at 268 and 303 (evand 1708 s for two counts, grid 73 s, selection about 1.5 min).
- Budget status: runnable, within the owner's standing 40 CPU-hour item cap.
- Possible subset under the cap: none needed.
- Depends on: H1 (think-hx0e) merged; #794 merged; the date 2026-10-26 UTC.
- Done when: the case at 268 holds T-242, select_houses --check passes with 268 off PENDING_ADOPTION, default_drawings --check-state passes, and the pull request lists the drawing before and after.
- Machine note: shares the four-core host; nice, at most 2 workers.

## Notes

2026-10-25, c-h2-268-1025: draft PR https://github.com/jlevy/squares/pull/807 (branch claude/intake-2026-10-26-t242-at-268), to merge on or after 2026-10-26T00:00Z. T-242 adopted at 268 in the pass of 26 October (LATER_PASSES['2026-10-26'] = {268}, prior-state archive 2026-10-26, stamp_landed --apply --date 2026-10-26), credit Daniel after Lavrentev; 268 off PENDING_ADOPTION. Regularized: grid-slack 1-degree view admitted (row 10) and drawn; Evan Daniel's same-side view at row 7 (review queue); no register candidate; about 4 CPU-minutes (packing/cases/regularized_drawings/think-3anz-2026-10-25/). Drawing before/after: grid-slack view of T-240 (19 uneven, 0 near-axis, 751 sides, 9 classes) to grid-slack view of T-242 (19, 0, 751, 12 classes). Also records #763's notebook-rows follow-up (issuecomment-6393433847) and the #797/#798 finals and closes. If main moves before the merge: merge it, stamp_landed --apply --date 2026-10-26, release_pin --update last.

2026-10-25 coord-intake-1024: #807 review A (issuecomment-6393871835) addressed; dispositions issuecomment-6393996400; head 9d1c4a357 (pin db18b3bcb), CI running (suite C pending at handback). Merges on 26 October UTC at the 00:10Z check-in (trig_0178kD4FUDrHjrZmrqD5uc12): if main moved, merge main, stamp_landed --apply (no --date), release_pin --update, CI, then merge. After the deploy: post the #763 follow-up (T-242 the house at 268; think-ptkk note) and record it.
