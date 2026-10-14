---
type: is
id: is-01m4vfsqg3sjnr9xrms9r3w7y3
title: Fable Max mathematical-correctness review of Fitzharding's sq17-lean, for sharing with the author
kind: task
status: open
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m4v5ne8b1dq1gyybx5mj689d
created_at: 2026-10-13T20:38:24.001Z
updated_at: 2026-10-14T00:59:16.644Z
---
Owner, 13 October: a strong Fable Max sub-agent for mathematical correctness on both n = 17 proofs, with full review docs to share back with the authors. Reviewer: tbd-strong-max on claude-fable-5-1, effort max, in /home/user/sq-math-fitzharding; deliverable docs/project/reviews/review-2026-10-13-fitzharding-n17-mathematical-correctness.md. Covers the checker-soundness modules and native_decide chain the intake review did not read; blind to that review until its findings are written.

## Notes

Done 14 October: docs/project/reviews/review-2026-10-13-fitzharding-n17-mathematical-correctness.md (in /home/user/sq-math-fitzharding, untracked; copy in the coordinator's scratchpad fable-reviews/). Verdict accepted, no blocking or major defect; MR-1 minor (stale docstrings), MR-2 to MR-6 notes; six questions for the author. Independent re-implementations replayed T1528/Node3, six chunk runs, freshCheck and summaryCheck with negative controls (scripts in scratchpad math-fitzharding/code/). Next: map it into T-154 (reviews, external_review), retain its programs as first-party receipts (OR-1), re-derive rungs (none moves: partial replays, no V3/C3), and draft the share-back to Fitzharding with the #565 reply.
