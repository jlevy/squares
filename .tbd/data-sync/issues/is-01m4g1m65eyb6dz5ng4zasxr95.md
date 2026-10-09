---
type: is
id: is-01m4g1m65eyb6dz5ng4zasxr95
title: Rebuild suite-file-costs record from a complete hosted cohort for mixed quick/slow modules
kind: task
status: open
priority: 3
version: 2
labels: []
dependencies: []
parent_id: is-01m4fdxw81pt2v4k29y9n58rn6
created_at: 2026-10-09T09:59:03.598Z
updated_at: 2026-10-09T11:54:24.004Z
---
test_confirm_gupta_records (~91 s hosted quick cost), test_ryxu_house_links (42 s), test_evand_arrangement_adoption (7 s), test_fn1_input_bindings (1 s) mix quick and slow tests, so admit-local (no -m filter) cannot measure their quick-lane cost; they stay unrecorded with no packing weight. Rebuild with suite_files record from the next complete green hosted cohort. Also: shard step walls in run 37910131315 were A 215 s, B 180 s, C 170 s, D 252 s against ceilings 143/168/168/143 (advisory on PRs).

## Notes

Follow-up review: main is at 9.8% unrecorded on suite shard 3/4 and every stack head at 9.6-9.7% against the 10% limit; one more unrecorded test file on main or a branch turns suite-a red. Per-layer admissions in stack 430 (#442 812dc2f26 ... #469 3fde0883b).
