---
type: is
id: is-01m32f1gyvq00kvmh9mab7jph9
title: C4 needs a first-party decision that does not inherit the reachable-cell idiom
kind: task
status: open
priority: 1
version: 1
labels: []
dependencies: []
parent_id: is-01m32dttakchrezsyqkyew4jet
created_at: 2026-09-21T17:08:28.247Z
updated_at: 2026-09-21T17:08:28.247Z
---
From the Fable proof review (verdict: admissible; V4; C3 on replay; C4 blocked).

Both Kleddamag checkers are implementations of ONE method: the same event / lazy-segment-tree / range-minimum sweep, sharing the bisect_right-1 / bisect_left reachable-cell idiom that our own kernel, R012 and R038 all share. The Python and JS slab counts differ by exactly 15706 = 2 x 7853, i.e. two interior polygon-vertex events per row -- a consistency check, not method independence. The threshold-box construction was ported by one author into both.

So agreement of the two replays is evidence against implementation slips, not against a shared method error. epistemics.md is literal: two independently written implementations of the same method derive C3, not C4.

For C4: decide the 7853 obligations with our interval branch-and-bound (threshold_interval) extended with per-row parent-centre envelopes and per-row (t, B). The threshold-atom support already exists from T-025. This is the same condition the handoff already set for T-031.
