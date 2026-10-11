---
type: is
id: is-01m3xkb16rqvby3jstb2cse70j
title: Update the n17 frontier record now that H-265 identifies S* with the catalogue polynomial
kind: task
status: open
priority: 2
version: 4
spec_path: packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-245-h265-n17-catalogue-polynomial.md
delegate: null
labels: []
dependencies: []
parent_id: is-01m3v9vq36ykk2jdzce75req44
hold: null
hold_until: null
created_at: 2026-10-02T06:03:03.768Z
updated_at: 2026-10-05T07:20:57.627Z
started_at: 2026-10-05T07:20:54.058Z
---
exp-245 accepted H-265. packing/frontier/n-017.md still says the identity with the degree-18 polynomial is not established (blocker detail near line 136; prose near lines 253, 612 and 642). Add an evidence entry for exp-245, narrow the blocker to global optimality, update the prose, and regenerate the frontier views; no bound or status change.

## Notes

2026-10-05. Delivered on PR 347 in 4c060f233: n-017.md (the blocker, the lead paragraph, the certified-endpoint section with a pointer to the explainer, the orientation sentence narrowed rather than reversed, and the degree-18 section), T-065's notes and next_rung, an annotation on E-n017-certified-endpoint, the new E-n017-catalogue-polynomial-identity (same-implementation, audited-here) and V-n17-catalogue-polynomial, with RESULTS.md, INVENTORY.md and VERIFIERS.md regenerated. The description's lines near 136, 253, 612 and 642 were 136-137, 253-254, 621-623 and 653-654, plus 634-635. Close when PR 347 merges.

2026-10-05 07:22 UTC (bead bookkeeper). Review B on jlevy/squares#347 (https://github.com/jlevy/squares/pull/347#pullrequestreview-5411026138) raised B4 (Medium) against this delivery: 4c060f233 is undisclosed in #347's body and unread by the register's usual reader. The reviewer found its evidential status consistent. The disclosure and the read are tracked by think-v3eq; this bead still closes when #347 merges.
