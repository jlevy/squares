---
type: is
id: is-01m0y6wad9gxebve4cs7sz3jqy
title: "Spike: attribute native Codex response timing fields"
kind: task
status: closed
priority: 0
version: 6
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-25-research-loop-efficiency-infrastructure.md
labels:
  - packing
  - focus-efficiency
  - spike
dependencies: []
parent_id: is-01m0r7q50gw0wepeaj1dzb7g3r
child_order_hints:
  - is-01m0y6wq9wen8qg1mmkm3vffy1
  - is-01m0y6wqq8eb3xjypgs1a8d2wz
  - is-01m0y6wr4ew7bebt57vamne60j
created_at: 2026-08-26T04:57:27.709Z
updated_at: 2026-08-26T05:37:23.179Z
closed_at: 2026-08-26T05:37:23.179Z
close_reason: CodexEfficiencyRollup/v2 now uses native duration and first-token telemetry, freezes live trees, excludes compressed legacy replay, reports recursive model/thinking timing, and the two named loops plus full local gate are measured and documented.
resolution: null
duplicate_of: null
---
Correct the efficiency scanner to consume native task_complete duration_ms and time_to_first_token_ms, preserve interval-based overlap accounting, and produce a recursive timing tree by session, model, and thinking level. Run the corrected scanner against Square packing research loops 1 and 2. Acceptance: red-green compatibility tests cover present, missing, and malformed native fields; the report quantifies coverage and reconciles client duration, first-token wait, timed model output, tool/CI time, and residual time without calling residual time model inference; the plan and review contain frozen measured rollups; no private JSONL or prose is committed.
