---
type: is
id: is-01m5qqwh830qd3x6f9qrga2tyz
title: "PR #795 (merge): follow-up review C of the W7 merge resolution (4ef6dedd0) and the review-B fixes"
kind: task
status: in_progress
priority: 1
version: 3
delegate: c-rev-795c-1024
labels: []
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-24T19:58:28.611Z
updated_at: 2026-10-24T20:14:52.219Z
started_at: 2026-10-24T19:58:33.893Z
---

## Notes

2026-10-24 c-rev-795c-1024: Review C (follow-up, round 2) of #795 at 439861d40, base 84d4a75af, published as a PR comment: https://github.com/jlevy/squares/pull/795#issuecomment-6389018390. Verdict: approve. C1 Low: W7's recipe-decision jobs key the release by label (beyond_horizon_replay.py:2624, :2640, :2681), latent since no push release has a recipe row. C2 Low: the walk README's generic 'the owner decides the credit' (intake_ledger.py:2831-2835) still stands over the five measured rows. W7 survived the merge 4ef6dedd0; B1, B2 and B3 hold, and B2 and B3 are red without their fixes. Scratch: rev-795c/.
