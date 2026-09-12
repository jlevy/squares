---
type: is
id: is-01m2ay2nyw6emx0zphn4pj685e
title: Meter and publish BC329 runner-stack resource usage separately
kind: task
status: in_progress
priority: 1
version: 5
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
updated_at: 2026-09-12T14:54:00.053Z
---
Treat the BC329 runner, calibration, and scientific continuation as a separate stacked-PR cost interval from PR148 and PR149. At each publication boundary, retain the native task-tree or agent rollups that are actually available, command wall times, validation shape, agent/model/effort assignments, and scientific target cost. Never infer missing token counts or mix earlier PR sessions into this layer. Update the runner PR's What This Branch Cost section and the relevant session/close report; finish with the record validators green.

## Notes

Stable partial native rollup through snapshot 2026-09-12T14:04:44.097Z: 13
completed BC329 task roots, 24 recursive sessions, 12,956.188 agent-active seconds
(3h35m56s), 12,545.538 summed active-union seconds, and 11,203.508
response-envelope seconds. Native counters by model and effort: Sol high 383 responses,
42,443,647 input / 41,504,896 cached input / 184,239 output / 79,102 reasoning
output; Sol xhigh 313, 42,956,913 / 41,737,344 / 161,621 / 92,924; Astra max
60, 5,945,303 / 5,549,824 / 42,882 / 16,884; Astra xhigh 35, 3,473,493 /
3,234,816 / 21,235 / 7,147; automatic approval review low 119, 9,134,010 /
8,209,664 / 12,160 / 4,913. Total: 910 responses, 103,953,366 input,
100,236,544 cached input, 422,137 output, and 200,970 reasoning output. Input
includes its cached subset; output includes its reasoning subset.

Included roots: 01a08cb9-50ef-7872-8e0a-c0c13baa7b11,
01a094fd-8f60-7b91-b2dd-9be9ba4470be,
01a0953a-c909-7b70-b076-27923f356cf7,
01a0953a-df69-7022-9d9d-21596fa3f2d1,
01a09560-c708-7cd1-8945-8f8d174e0a4f,
01a09565-6772-7fd2-9708-d7d47e01527c,
01a09572-7c3d-7da0-9a43-165190e57274,
01a0957b-66e1-7512-b026-b9eb28271364,
01a095ce-d452-78a1-a1d4-e6dffc857781,
01a095ce-ee27-70a3-bb60-1fe446d5aacc,
01a095cf-374d-7552-a1db-0d30bb3f4083,
01a095df-849e-7cb0-a9cb-68bc1549f3e9, and
01a095e3-26ce-7cf2-913f-31080807643f.

Excluded until the next stable boundary: live preflight re-review, calibration repair,
documentation correction, and their descendants. The shared coordinator root
01a082b3-057c-7c62-905c-1a543979e33a remains excluded because its log also contains
PR #149 work and has no branch telemetry. Do not infer an allocation.

Local validation is accounted separately in PR #156. The baseline branch's valid
merged-head pre-push passed 46/74 named steps in 1,118.89 seconds with 5,156 tests,
3 platform skips, 57 deselections, Ruff clean over 1,784 files, and BasedPyright at
zero. Hosted CI was green at 5fa83cc7. The PR body also retains four invalid or
sandbox-constrained attempts and their exact costs rather than folding them into the
valid gate. No BC329 scientific target has run.
