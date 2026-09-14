---
type: is
id: is-01m2ay2nyw6emx0zphn4pj685e
title: Keep PR156 runner-stack usage current through merge
kind: task
status: in_progress
priority: 1
version: 12
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
delegate: root accounting lane
labels:
  - n11
  - usage
dependencies:
  - type: blocks
    target: is-01m2axbxf0xz00ezc32q4mesn2
  - type: blocks
    target: is-01m2eddtqbpv11d9g5yk0s8cv0
  - type: blocks
    target: is-01m2ett207c0f76hc55gp435wz
parent_id: is-01m26c1jahzgfckegz7fp9wcq7
created_at: 2026-09-12T13:49:28.411Z
updated_at: 2026-09-14T02:28:04.889Z
---
Treat the BC329 runner, calibration, and scientific continuation as a separate stacked-PR cost interval from PR148 and PR149. At each publication boundary, retain the native task-tree or agent rollups that are actually available, command wall times, validation shape, agent/model/effort assignments, and scientific target cost. Never infer missing token counts or mix earlier PR sessions into this layer. Update the runner PR's What This Branch Cost section and the relevant session/close report; finish with the record validators green.

## Notes

Historical Sep12 14:04:44.097 UTC subtotal: 13 completed BC329 roots, 24 recursive sessions, 910 responses, 103,953,366 input (100,236,544 cached), 422,137 output (200,970 reasoning), 12,956.188 summed agent-active seconds. Sol high independently recovered and reproduced all 13 root IDs from tbd-sync commit 90fa7cda9d3bdec31f3dc9dda8987b2c3da67815, file .tbd/data-sync/issues/is-01m2ay2nyw6emx0zphn4pj685e.md; maintained scanner exactly reproduced every saved counter and found zero incomplete sessions. Operator-selected task ownership includes n11_next_slice_strategy because logs lack branch telemetry. Sep13 audit through 19:30:30 UTC selected 27 further disjoint complete PR156-only roots, 62 sessions, 2,191 responses, 258,809,511 input (247,444,992 cached), 1,125,247 output (448,041 reasoning), 41,905.847 active seconds. Conservative additive selected subtotal: 40 roots, 86 sessions, 3,101 responses, 362,762,877 input (347,681,536 cached), 1,547,384 output (649,011 reasoning), 54,862.035 active seconds. Exact 27 roots and exclusions are in docs/project/reviews/review-2026-09-13-pr156-usage-delta.md and PR156 draft body. Mixed coordinator, two incomplete trees, ambiguous branch ownership, BC303 T1/T2, PR149/157, postcutoff work excluded. No full branch bill or scientific target cost claimed.

Sep13 local PR156 refresh through 22:29:00 UTC: 10 additional disjoint complete direct-child roots, 11 recursive sessions, 446 native responses, 47,504,641 input (46,383,872 cached), 142,441 output (52,908 reasoning), and 4,541.654 summed agent-active seconds. The new-slice active wall union is 3,991.479 seconds and first-to-last envelope is 10,053.921 seconds; neither is additive to older wall figures. Conservative selected cumulative subtotal: 50 roots, 97 sessions, 3,547 responses, 410,267,518 input (394,065,408 cached), 1,689,825 output (701,919 reasoning), 59,403.689 summed agent-active seconds. Exact new IDs, method, exclusions, and numeric output are /private/tmp/pr156-usage-refresh-note.md and /private/tmp/pr156-usage-refresh.json; cost-first PR body draft is /private/tmp/pr156-body-cost-first-draft.md. Local head 2f8925b2 is clean against merged origin/main f2e24e07 (57 files, +31,868/-169). Records 32/74 and edit 45/74 pass; local --push was red on three sandbox-dependent reachable controls (1,590 passed, 3 skipped, 6 deselected); unrestricted --push and exact-head hosted CI remain pending. No BC329 scientific target was run. Mixed coordinator, previously scanner-incomplete or ambiguous BC329 roots, PR157, T1/T2/H161, and activity after cutoff remain excluded. This does not infer a full branch bill.


2026-09-14: re-scoped. Its dependency on think-17qa (run the BC329 target) dated from 2026-09-12 when this bead included target cost; it made the post-merge checkpoint think-088v unable to close until BC329 ran. The owner deferred BC329 (think-zwlf), so this bead now covers only the #156 cost section through merge (the body's native subtotal stops at 2026-09-13 22:29 UTC). Target cost, if BC329 is ever revived, belongs to a new bead blocked by think-17qa.
