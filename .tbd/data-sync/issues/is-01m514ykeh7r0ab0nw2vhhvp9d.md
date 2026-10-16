---
type: is
id: is-01m514ykeh7r0ab0nw2vhhvp9d
title: "PR #636 A7: per-count run outcomes in the index are deferred with no bead"
kind: bug
status: closed
priority: 3
version: 3
delegate: ecstatic-edison-636-review-a
labels:
  - regularization
dependencies: []
parent_id: is-01m514y11gd146dzhmnf7ke508
hold: null
hold_until: null
created_at: 2026-10-16T01:24:15.953Z
updated_at: 2026-10-16T02:07:13.637Z
started_at: 2026-10-16T01:24:36.107Z
closed_at: 2026-10-16T02:07:13.637Z
close_reason: "Deferred (PR #636 A7): the work is tracked by think-4ov9 (open, under think-sfas): record per-count run outcomes on each index entry so a decision needs no SETTLED entry; waits on #636 merging. Named in SETTLED's comment (288a1a520), the guide and the PR body's Limits."
resolution: null
duplicate_of: null
---
Low. PR body Limits; default_drawings.py:163-168. Fix: open a bead for recording per-count decisions on each index entry from the reports layer reads; name it in the SETTLED comment and the Limits section. Review: https://github.com/jlevy/squares/pull/636#pullrequestreview-5541598868
