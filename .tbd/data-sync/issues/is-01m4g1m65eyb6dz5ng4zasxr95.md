---
type: is
id: is-01m4g1m65eyb6dz5ng4zasxr95
title: Rebuild suite-file-costs record from a complete hosted cohort for mixed quick/slow modules
kind: task
status: in_progress
priority: 3
version: 5
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m4fdxw81pt2v4k29y9n58rn6
hold: null
hold_until: null
created_at: 2026-10-09T09:59:03.598Z
updated_at: 2026-10-09T18:47:14.536Z
started_at: 2026-10-09T13:00:58.669Z
---
test_confirm_gupta_records (~91 s hosted quick cost), test_ryxu_house_links (42 s), test_evand_arrangement_adoption (7 s), test_fn1_input_bindings (1 s) mix quick and slow tests, so admit-local (no -m filter) cannot measure their quick-lane cost; they stay unrecorded with no packing weight. Rebuild with suite_files record from the next complete green hosted cohort. Also: shard step walls in run 37910131315 were A 215 s, B 180 s, C 170 s, D 252 s against ceilings 143/168/168/143 (advisory on PRs).

## Notes

Follow-up review: main is at 9.8% unrecorded on suite shard 3/4 and every stack head at 9.6-9.7% against the 10% limit; one more unrecorded test file on main or a branch turns suite-a red. Per-layer admissions in stack 430 (#442 812dc2f26 ... #469 3fde0883b).

2026-10-09 #469 53900e4ea run 37932934865: suite-d wall 288.47 s vs 143 s ceiling (202%, over the 2x PR backstop) with every test passing; round 5 at #469 read A 228.9 / B 308.1 / C 254.0 / D 169.3, round 6 A 217.9 / B 164.8 / C 247.6 / D 288.5 (partition imbalance; unweighted mixed modules incl. test_confirm_gupta_records ~91 s land in D). Rebalance via suite_files record from hosted cohorts at #469 in progress.

Owner chose (in session) to land the rebalance and keep the per-layer raw admission reports. #469 600068983: suite_files record --shards 4 --target-ceilings 131,154,154,131 over run 37932934865's four cohort reports (708 files; predicted 730.6/858.9/858.9/730.6); 29 local admissions superseded by hosted weights for the same 42 modules; check exit 0; 67 tests pass. Structural overload remains: lane ~3,200-3,500 test-seconds vs ~2,150 ceiling capacity, so a ~1.25x slow runner can still reach the 2x backstop on any shard (owner decision under think-be1s / think-p684: fifth shard or ceilings).
