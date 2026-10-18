---
type: is
id: is-01m57pjpenj2sq63cvqhtv2v8w
title: "PR #665: bound subprocess-probe ownership and isolate the pool lane"
kind: bug
status: in_progress
priority: 2
version: 2
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m57j9xsga57szgfah5ex2bcd
hold: null
hold_until: null
created_at: 2026-10-18T14:27:46.772Z
updated_at: 2026-10-18T14:28:02.100Z
started_at: 2026-10-18T14:28:02.099Z
---
Own only packing/tests/test_suite_files.py. Five nested-pytest definitions timed out at 60 seconds under the broad nine-worker gate while focused seven-item runs pass in 2.63 seconds serial and 3.48 seconds at nine workers. Mark these real subprocess controls pool_heavy without raising the deadline, ensure every launched sibling is killed and reaped after timeout/assertion failures, add focused cleanup evidence, and commit only this file. No broad gate or GitHub mutation in this slice.
