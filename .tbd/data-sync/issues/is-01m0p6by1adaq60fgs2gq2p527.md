---
type: is
id: is-01m0p6by1adaq60fgs2gq2p527
title: "PR #5 review F-5: overlap guard asserted against a drifting accumulator"
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m0p6bwcyve6zdv41ezr08e3g
created_at: 2026-08-23T02:14:35.297Z
updated_at: 2026-08-23T02:14:35.297Z
---
search.rs maintains overlap incrementally over ~4e5 steps per anneal and snapshots the accumulator at record time, never recomputing from the stored best. FEASIBLE_EPS=1e-12 is at the plausible scale of accumulated cancellation error, which can drift either way. Two adjacent nits: stored energy goes stale as lambda ramps; the budget check lets a chain overshoot by up to one anneal.
