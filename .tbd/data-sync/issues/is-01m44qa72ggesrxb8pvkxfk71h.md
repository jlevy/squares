---
type: is
id: is-01m44qa72ggesrxb8pvkxfk71h
title: "PR #336 A4 (Low): reporting and private APIs."
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
created_at: 2026-10-05T00:27:12.335Z
updated_at: 2026-10-05T05:23:26.352Z
started_at: 2026-10-05T02:30:55.897Z
closed_at: 2026-10-05T02:56:31.435Z
close_reason: "Review A fixed in 49613a52f: 21 local controls, three hosted native cases, lint/types/docs, all current required checks PASS; await Joshua, no follow-up reserved."
resolution: null
duplicate_of: null
---
https://github.com/jlevy/squares/pull/336#pullrequestreview-5408660754

**A4 (Low): reporting and private APIs.**
- Line 647: a root that exits 0 reports `success` even when live descendants are killed at cleanup. Only `active_processes_before_cleanup` records it.
- `process_handle` (line 43) reads CPython's private `Popen._handle`.
- Resume uses the undocumented `NtResumeProcess`.
- All acceptable, but say so in the docs.

Authorized maintenance only. Disposition requires evidence and exact-head CI; no research follow-up reserved.

## Notes

Claude follow-up 2026-10-05: 24d3d98f7 adds the success-with-cleanup status (exit 0) for a root that exits zero with live descendants terminated, bumps receipts to packing.windows-supervisor.v2, and documents Popen._handle and NtResumeProcess in the docstrings.
