---
type: is
id: is-01m44qa6a9k1nwkctp9e9jx412
title: "PR #336 A3 (Low): the author's machine policy is hard-coded."
kind: task
status: closed
priority: 2
version: 4
delegate: graph_gate
labels: []
dependencies: []
parent_id: is-01m44qa2mz6hseqc8b10neq6b3
hold: null
hold_until: null
created_at: 2026-10-05T00:27:11.560Z
updated_at: 2026-10-05T05:23:24.509Z
started_at: 2026-10-05T02:30:55.205Z
closed_at: 2026-10-05T02:56:30.732Z
close_reason: "Review A fixed in 49613a52f: 21 local controls, three hosted native cases, lint/types/docs, all current required checks PASS; await Joshua, no follow-up reserved."
resolution: null
duplicate_of: null
---
https://github.com/jlevy/squares/pull/336#pullrequestreview-5408660754

**A3 (Low): the author's machine policy is hard-coded.**
- `supervise_windows.py:794` refuses whenever `--min-available-gib` is below 8 and only allows tightening, so a host with under 8 GiB free can never use the tool.
- The review threshold (default 12, line 763) always fires before the stop threshold (default 16, line 757), so the 16 GiB stop is unreachable by default.

Authorized maintenance only. Disposition requires evidence and exact-head CI; no research follow-up reserved.

## Notes

Claude follow-up 2026-10-05: 24d3d98f7 names the defaults (DEFAULT_WORKER_MEMORY_GIB 16, DEFAULT_REVIEW_MEMORY_GIB 12, DEFAULT_MIN_AVAILABLE_GIB 8). The review threshold is now a non-terminating mark (recorded and warned about), so both thresholds are reachable at the defaults. A lowered floor, or a review mark at or above the stop, warns via stderr and guard_warnings rather than refusing.
