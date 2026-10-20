---
type: is
id: is-01m4sypecqzbpb53pmv8wgkzy6
title: release_pin --update can leave a stale release.pyc that tests then import
kind: bug
status: open
priority: 3
version: 1
labels:
  - tooling
dependencies: []
created_at: 2026-10-13T06:20:16.151Z
updated_at: 2026-10-13T06:20:16.151Z
---
devtools.release_pin imports sqpack.release (compiling release.py to __pycache__) and then rewrites the DATA_REVISION line: one 40-hex hash for another, so the file keeps its byte size, and the rewrite can land in the same second as the compile. CPython's default pyc invalidation compares source mtime (seconds) and size, so the stale .pyc is accepted and tests/test_release.py::test_the_pinned_data_revision_is_the_last_data_commit then reads the old pin and fails locally although release.py is correct (seen 2026-10-13 on #560 at 2e7e55db1; fresh CI checkouts are unaffected). Fix: have release_pin remove or invalidate sqpack/__pycache__/release.*.pyc after writing (or bump the mtime past the compile), and say so in its docstring.
