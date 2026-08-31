---
type: is
id: is-01m0w1b99ha5rrbrhxre02tesx
title: Refresh four stale numeric negative-control anchors
kind: bug
status: closed
priority: 1
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels: []
dependencies: []
parent_id: is-01m0vr7g27g67p699aepcdksxd
created_at: 2026-08-25T08:42:17.772Z
updated_at: 2026-08-25T08:43:46.065Z
closed_at: 2026-08-25T08:43:46.064Z
close_reason: "Completed: updated all four stale anchors to the final post-D-255 values and reran the exact failed step from stable files; all 62 negative controls fire in 12.91 wall seconds. D-255 records the D-198 recurrence."
resolution: null
duplicate_of: null
---
CI run 32827545803 failed on Linux and macOS because four controls.yaml exact anchors lagged the current defect count, synopsis date, soundness-direction aggregate, and gate-detector aggregate. Update anchors to the final post-D-255 state, run the negative-control suite, and retain the recurrence in defects.yaml.
