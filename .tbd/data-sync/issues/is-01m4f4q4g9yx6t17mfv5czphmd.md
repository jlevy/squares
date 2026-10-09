---
type: is
id: is-01m4f4q4g9yx6t17mfv5czphmd
title: Preserve complete n17 ten-shard census while fixing intake full-gate per-test ceiling
kind: bug
status: in_progress
priority: 1
version: 2
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4ekeq41zfgtf5dp8r462n05
hold: null
hold_until: null
created_at: 2026-10-09T01:33:51.496Z
updated_at: 2026-10-09T01:36:18.384Z
started_at: 2026-10-09T01:36:18.370Z
---
Actual PR440 head9425a4698964d1b9443627d755a87a6ad23ac364 full run37866268669 validate job113613623484 fails the unchanged12-second per-test guard: tests/test_survey_n17_residue.py::test_ten_shards_cover_the_distance_two_frame_once measured12.37s. All11 scientific jobs pass; this is a genuine engineering timing failure, not a mathematical counterexample. Astra reviews immutable targeted source for redundant work; Sol will implement only a measured semantics-preserving optimization, retaining complete ten-shard distance-two frame census, every assertion, source inputs and12s ceiling. No blind retry, sampling, cap relaxation or foreign active n17 worktree edits. Preserve failed425142-byte job log in review-notes/pr440-9425-full-validate-failure.log; actual corrected-head required/Pages/full gates and independent review are required before merge.
