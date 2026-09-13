---
type: is
id: is-01m2ay2nyw6emx0zphn4pj685e
title: Meter and publish BC329 runner-stack resource usage separately
kind: task
status: in_progress
priority: 1
version: 6
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
delegate: root accounting lane
labels:
  - n11
  - usage
dependencies:
  - type: blocks
    target: is-01m2axbxf0xz00ezc32q4mesn2
parent_id: is-01m26c1jahzgfckegz7fp9wcq7
created_at: 2026-09-12T13:49:28.411Z
updated_at: 2026-09-13T19:41:27.944Z
---
Treat the BC329 runner, calibration, and scientific continuation as a separate stacked-PR cost interval from PR148 and PR149. At each publication boundary, retain the native task-tree or agent rollups that are actually available, command wall times, validation shape, agent/model/effort assignments, and scientific target cost. Never infer missing token counts or mix earlier PR sessions into this layer. Update the runner PR's What This Branch Cost section and the relevant session/close report; finish with the record validators green.

## Notes

Historical Sep12 14:04:44.097 UTC subtotal remains 13 completed BC329 roots/24 recursive sessions/910 responses/103,953,366 input (100,236,544 cached)/422,137 output (200,970 reasoning)/12,956.188 summed agent-active seconds. Independent Sep13 audit through 19:30:30 UTC selected 27 disjoint scanner-complete PR156-only roots/62 sessions and measured 2,191 responses, 258,809,511 input (247,444,992 cached), 1,125,247 output (448,041 reasoning), 41,905.847 summed active seconds. Additive conservative selected subtotal: 40 roots/86 sessions/3,101 responses/362,762,877 input (347,681,536 cached)/1,547,384 output (649,011 reasoning)/54,862.035 active seconds. Exact 27 roots and exclusions retained in docs/project/reviews/review-2026-09-13-pr156-usage-delta.md (local PR156 branch until push) and draft PR body. Mixed coordinator, two incomplete roots, ambiguous PR ownership, BC303 T1/T2, PR149/157, and postcutoff work excluded. No full branch bill or scientific target cost claimed.
