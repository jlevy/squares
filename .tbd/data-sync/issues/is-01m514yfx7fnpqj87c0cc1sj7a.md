---
type: is
id: is-01m514yfx7fnpqj87c0cc1sj7a
title: "PR #636 A2: PENDING_ALLOWED is not shrink-only, and nothing checks its beads are open"
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
created_at: 2026-10-16T01:24:12.327Z
updated_at: 2026-10-16T02:07:02.815Z
started_at: 2026-10-16T01:24:31.917Z
closed_at: 2026-10-16T02:07:02.815Z
close_reason: "Fixed (PR #636 A2) in 288a1a520: policy wording in the pass message, step comment, test name and PR body; gate prints the list size; PENDING_ALLOWED, exemption and owed beads are deferrals check_bead_tree holds open (default_drawings.deferrals, regularization_deferrals; default_drawings.py in DEFERRAL_RECORDS). Tests: test_the_record_defers_each_count_to_the_bead_that_owns_it, test_bead_tree cases."
resolution: null
duplicate_of: null
---
Medium. packing/devtools/default_drawings.py:782-798,:131,:814-817; packing/src/sqpack/cli/validate.py:3800; packing/tests/test_default_drawings.py:250. Fix: use the policy's wording (the list equals the pending set; a count joins only by a reviewed change naming its bead); hold each PENDING_ALLOWED and EXEMPT entry to an open bead through check_bead_tree's deferral machinery (DEFERRAL_RECORDS); print the allowed total. Review: https://github.com/jlevy/squares/pull/636#pullrequestreview-5541598868
