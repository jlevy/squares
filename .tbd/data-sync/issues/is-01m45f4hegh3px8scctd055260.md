---
type: is
id: is-01m45f4hegh3px8scctd055260
title: "PR #350 B2 (Medium): replace the retracted 'ten times more of the tree per node' sentence with wand125's correction"
kind: task
status: closed
priority: 2
version: 3
spec_path: docs/project/reviews/review-2026-10-02-n17-bulk-exclusion-design.md
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m45f4dj0p0t4bsxjnxcz5whv
hold: null
hold_until: null
created_at: 2026-10-05T07:23:32.176Z
updated_at: 2026-10-05T07:27:35.033Z
started_at: 2026-10-05T07:27:29.552Z
closed_at: 2026-10-05T07:27:35.028Z
close_reason: "Fixed in #350's body, edited 2026-10-05T07:01:17Z by jlevy (before Review B was submitted at 07:04 but after the reviewer read it): Limits now carries wand125's correction of 2026-10-05 (search-order artefact; 2.17% vs 2.05% of W7 single-threaded at 1 M nodes; Knuth's estimate ~40,000 vs ~138,000 nodes on A), and the retracted 'ten times more of the tree per node' sentence appears nowhere else (checked 07:40 UTC). Body edit, no branch commit."
resolution: null
duplicate_of: null
---
Review B finding B2 on jlevy/squares#350 (https://github.com/jlevy/squares/pull/350#pullrequestreview-5411026984), at head 9179aab7d. Limits says the specification-only prover 'closes about ten times more of the tree per node than the existing relaxation'. wand125's comment of 2026-10-05 02:41 UTC on #350 retracts it as a search-order artefact: single-threaded at 1 M nodes the two close 2.17% and 2.05% of W7; Knuth's estimate puts the existing tree on A at about 40,000 nodes against 138,000 for the other prover. Fix: replace the sentence with the correction.
