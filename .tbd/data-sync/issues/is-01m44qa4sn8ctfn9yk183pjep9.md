---
type: is
id: is-01m44qa4sn8ctfn9yk183pjep9
title: "PR #336 A1 (Medium): no gate exercises the native path."
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
created_at: 2026-10-05T00:27:10.005Z
updated_at: 2026-10-05T05:23:20.564Z
started_at: 2026-10-05T02:30:53.819Z
closed_at: 2026-10-05T02:56:29.347Z
close_reason: "Review A fixed in 49613a52f: 21 local controls, three hosted native cases, lint/types/docs, all current required checks PASS; await Joshua, no follow-up reserved."
resolution: null
duplicate_of: null
---
https://github.com/jlevy/squares/pull/336#pullrequestreview-5408660754

**A1 (Medium): no gate exercises the native path.**
- All the FFI and Job-object lifecycle code (`devtools/supervise_windows.py`, about 821 lines of ctypes) is covered only by 3 Windows-only tests, which skip on Linux (`tests/test_supervise_windows.py:136`).
- The acceptance evidence is the author's local receipts. This conflicts with OR-13.
- **Fix:** add a small `windows-latest` CI job for the 3 native tests (about 3 s), or state explicitly that native acceptance is not gated.

Authorized maintenance only. Disposition requires evidence and exact-head CI; no research follow-up reserved.

## Notes

Claude follow-up 2026-10-05 (session_015emxaK1NvNvrM2nxfYgF4L): 24d3d98f7 path-filters the Windows workflow and sets timeout-minutes 5; a portable contract test holds its pins, interpreter, paths, ceiling and native case count. It stays outside gate-budgets.yaml (registering it would take an aggregator, a wall-check step, a CI_EVENTS entry and samples). Native job at 058434d09: 3 passed, 23 deselected, 54 s wall (run 37267152904).
