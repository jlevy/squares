---
type: is
id: is-01m58dfyf99t7khbxj1th335af
title: "PR #406 S1: bound both Git metadata streams during capture"
kind: bug
status: in_progress
priority: 1
version: 2
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4mv0ysrv4te0kgnpxn0wfwp
hold: null
hold_until: null
created_at: 2026-10-18T21:08:13.927Z
updated_at: 2026-10-18T21:08:20.465Z
started_at: 2026-10-18T21:08:20.463Z
---
Security preflight S1 at PR #406 head 8811bd763d437aaf8d75dc5d1dd4ac761a1bc39d: packing/devtools/check_added_blobs.py:_git currently uses subprocess.run(capture_output=True), buffering unlimited stdout and stderr before checking MAX_METADATA_BYTES. Consume both streams concurrently with an enforced per-stream cap, kill/reap the child immediately on excess, retain the existing deadline and fail-closed errors, and add focused small-cap oversized-stdout/stderr regressions proving early termination in packing/tests/test_added_blob_guard.py. Coordinator root owns publishing and schedules focused tests after #676 Stage 3 releases the heavy slot.
