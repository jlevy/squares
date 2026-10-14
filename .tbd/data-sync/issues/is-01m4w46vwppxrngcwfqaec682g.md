---
type: is
id: is-01m4w46vwppxrngcwfqaec682g
title: "PR #592 A1: proof-assistant kind test reads the target's cited evidence, not the second proof's own"
kind: bug
status: closed
priority: 1
version: 4
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4w0w8x81jgrxwd2dshv8f0v
hold: null
hold_until: null
created_at: 2026-10-14T02:35:06.006Z
updated_at: 2026-10-14T09:00:15.071Z
started_at: 2026-10-14T02:35:14.134Z
closed_at: 2026-10-14T09:00:15.071Z
close_reason: PR592 Review A dispositions published6163321688 and confirmed by independentD/F/G; all current-head CI+full38530454327 pass, mergedf73 and Pagesdeploymentverified38536230832. Full proof replays remain separately deferred; V0/C1 unchanged.
resolution: null
duplicate_of: null
---
Medium. packing/devtools/check_results.py:872-885, epistemics.md:456-458. Fix: test only the second proof's own evidence (exclude entries cited by the named results); tests for a paper simplification citing a Lean-checked target entry (accepted) and a formalization whose only proof-assistant entry is the target's (refused). Review A (senior, round 1, head 7a1aadceb), PR #592: https://github.com/jlevy/squares/pull/592#issuecomment-6159185393
