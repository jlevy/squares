---
type: is
id: is-01m4ez7rb03vgyshp0cjw0b2vc
title: Correct n211 to a horizontal flip matching n241 orientation
kind: bug
status: in_progress
priority: 2
version: 2
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4e35s7r1e65r1qmpz250h0p
hold: null
hold_until: null
created_at: 2026-10-08T23:58:04.639Z
updated_at: 2026-10-08T23:58:12.084Z
started_at: 2026-10-08T23:58:12.083Z
---
The user reports that the earlier vertical reflection left n=211 in the wrong orientation and now explicitly requests a horizontal flip so it looks like n=241. Delegate correction to a subagent. Compare current, immutable parent and n=241 geometry before choosing the source-bound transform; replace the old reflection rather than accidentally compounding it. Apply consistently to selected and exact drawings and all recorded escape directions, preserving side bounds, scientific claims, source evidence, IDs/dates and the other 323 cases. Verify exact geometry and replay invariance, retain a visual comparison, update canonical n211 records/renderings through maintained scoped tools, then refresh release data pin/composites and preview when final exports can proceed. Keep the row-spacing work parallel with disjoint ownership.
