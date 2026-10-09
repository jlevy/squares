---
type: is
id: is-01m4ey826ykymayr66y0fz3f55
title: Resolve Gupta-layer native house-reader wall failure within 12 seconds
kind: bug
status: in_progress
priority: 1
version: 3
assignee: intake_remaining_fixes
delegate: codex@spud10.local
labels:
  - result-import
dependencies: []
parent_id: is-01m4ekeq41zfgtf5dp8r462n05
child_order_hints:
  - is-01m4f4f0xr1v7nybt5qjgt2x2n
hold: null
hold_until: null
created_at: 2026-10-08T23:40:46.173Z
updated_at: 2026-10-09T01:29:25.685Z
started_at: 2026-10-08T23:40:57.272Z
---
The actual old PR448 head 13a53457549b62b56b3573d1c77a638ada0f9573 failed its full checkpoint run 37852701067, validate job 113569389039: https://github.com/jlevy/squares/actions/runs/37852701067/job/113569389039. Fast behavioral shard D reported tests/test_negative_controls.py::test_second_squish_consumers_survive_native_worker_boundaries[house-reads] at 14.01 seconds, exceeding the unchanged 12-second per-test wall ceiling. This is a real performance-guard failure, not a passing assertion result or an infrastructure disposition.

The existing intake_remaining_fixes lane owns investigation and a bounded correction, with a read-only Gupta design opinion and independent Astra review. Keep the full actual production clone, complete protected/private input custody, fresh native worker boundary, both current-house refusals and all nine retained-house admissions. Preserve all scientific/source bytes, native outcomes, admission premises and the 12-second ceiling. The guard already reuses one real complete SQUISH admission while rechecking loaded functions/constants and every protected input byte/path before returning a deep copy. Do not reduce the Gupta history roster or inherit a cache without binding all its premises.

A profile of the exact existing native child is required before claiming a concrete optimization. External disk exhaustion currently blocks the roughly 200 MiB actual clone; no internal-disk fallback, new whole-source copies, broad tests, threshold changes or blind CI reruns. Source correction remains pending disk recovery and measured evidence. Parent think-mx4n coordinates the normal-merge cascade and exact-head hosted gates; this node must receive an explicit passing disposition before the owning layer is merged.
