---
type: is
id: is-01m514ygmrqm3trjaf2929d9r5
title: "PR #636 A3: no test drives a regularized count to pending through the real derivation; nothing tests admit_views strips the lapse"
kind: bug
status: closed
priority: 2
version: 3
delegate: ecstatic-edison-636-review-a
labels:
  - regularization
dependencies: []
parent_id: is-01m514y11gd146dzhmnf7ke508
hold: null
hold_until: null
created_at: 2026-10-16T01:24:13.080Z
updated_at: 2026-10-16T02:07:03.612Z
started_at: 2026-10-16T01:24:32.467Z
closed_at: 2026-10-16T02:07:03.612Z
close_reason: "Fixed (PR #636 A3) in 288a1a520 and d76f322f2: test_an_adoption_that_rebuilds_only_the_axis_view_reads_pending (real derivation, temp index) and test_an_admitted_view_ends_the_lapse_the_axis_record_carried; three mutations each fail them."
resolution: null
duplicate_of: null
---
Medium. packing/tests/test_default_drawings.py:177-339; packing/devtools/regularize_evand.py:3347. Fix: replay the axis-only adoption on a tmp index (reference + lapse_of), assert state_problems reports 'draws another view', count_state reads pending, and state_problems fails 'n=<n> is pending'; fixture test that admit_views writes a reference without lapsed. Review: https://github.com/jlevy/squares/pull/636#pullrequestreview-5541598868
