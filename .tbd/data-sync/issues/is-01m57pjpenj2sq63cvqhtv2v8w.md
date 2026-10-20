---
type: is
id: is-01m57pjpenj2sq63cvqhtv2v8w
title: "PR #665: bound subprocess-probe ownership and isolate the pool lane"
kind: bug
status: closed
priority: 2
version: 3
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m57j9xsga57szgfah5ex2bcd
hold: null
hold_until: null
created_at: 2026-10-18T14:27:46.772Z
updated_at: 2026-10-18T14:31:55.700Z
started_at: 2026-10-18T14:28:02.099Z
closed_at: 2026-10-18T14:31:55.684Z
close_reason: "Committed b88568f9a09d7a17100432c4ba9b08b392d5da9f; only packing/tests/test_suite_files.py (+97/-9). Five existing subprocess definitions/seven items moved to pool_heavy without changing the 60s deadline. ExitStack owns and reaps every launched sibling. Two real-child timeout/assertion cleanup regressions failed before repair and pass afterward. Owned module: 69 passed in 3.74s; pool collection 9/69; Ruff clean; BasedPyright 0 errors, warnings, notes; normal commit hooks passed in 11.28s. Uncommitted-scope review found no remaining issues; no documentation behavior changed. No broad gate or remote publication in this slice."
resolution: null
duplicate_of: null
---
Own only packing/tests/test_suite_files.py. Five nested-pytest definitions timed out at 60 seconds under the broad nine-worker gate while focused seven-item runs pass in 2.63 seconds serial and 3.48 seconds at nine workers. Mark these real subprocess controls pool_heavy without raising the deadline, ensure every launched sibling is killed and reaped after timeout/assertion failures, add focused cleanup evidence, and commit only this file. No broad gate or GitHub mutation in this slice.
