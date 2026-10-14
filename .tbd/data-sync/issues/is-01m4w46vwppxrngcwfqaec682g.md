---
type: is
id: is-01m4w46vwppxrngcwfqaec682g
title: "PR #592 A1: proof-assistant kind test reads the target's cited evidence, not the second proof's own"
kind: bug
status: in_progress
priority: 1
version: 2
delegate: addresser-592-review-a
labels: []
dependencies: []
parent_id: is-01m4w0w8x81jgrxwd2dshv8f0v
hold: null
hold_until: null
created_at: 2026-10-14T02:35:06.006Z
updated_at: 2026-10-14T02:35:14.134Z
started_at: 2026-10-14T02:35:14.134Z
---
Medium. packing/devtools/check_results.py:872-885, epistemics.md:456-458. Fix: test only the second proof's own evidence (exclude entries cited by the named results); tests for a paper simplification citing a Lean-checked target entry (accepted) and a formalization whose only proof-assistant entry is the target's (refused). Review A (senior, round 1, head 7a1aadceb), PR #592: https://github.com/jlevy/squares/pull/592#issuecomment-6159185393
