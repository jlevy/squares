---
type: is
id: is-01m0wz3mcfdc54c3q1npkv5t4h
title: Tutorial conflated the 1e-11 side floor with the 1e-10 feasibility tolerance
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m0wy9s97fwegw5kqrge2p8sy
created_at: 2026-08-25T17:22:24.270Z
updated_at: 2026-08-25T17:49:30.171Z
closed_at: 2026-08-25T17:49:30.170Z
close_reason: Fixed on the PR 33 branch; see review-2026-08-25-tutorial-soundness-iteration-2.md and defects D-320..D-328. Full gate green.
resolution: null
duplicate_of: null
---
TUTORIAL.md section 8 open item 5 said the floor IS HiGHS's feasibility tolerance pinned at the strictest accepted value. quench.py pins primal/dual feasibility at 1e-10 (the strictest HiGHS accepts); the 1e-11 figure is the post-checked side-residual floor that tolerance produces (SYNOPSIS line ~1224). Fixed to state the mechanism.
