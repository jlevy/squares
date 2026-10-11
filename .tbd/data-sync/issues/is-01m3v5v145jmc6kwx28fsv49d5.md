---
type: is
id: is-01m3v5v145jmc6kwx28fsv49d5
title: test_migrate_math uses GNU sed -i and fails on macOS
kind: bug
status: closed
priority: 3
version: 2
labels: []
dependencies: []
created_at: 2026-10-01T07:28:38.968Z
updated_at: 2026-10-06T08:50:43.292Z
closed_at: 2026-10-06T08:50:43.291Z
close_reason: "Done: packing/tests/test_migrate_math.py on origin/main (replaced by #254, merged 2026-10-01) no longer contains the GNU 'sed -i' fake formatter."
resolution: null
duplicate_of: null
---
tests/test_migrate_math.py::test_apply_refuses_when_the_formatter_would_change_a_span writes a fake formatter with sed -i \"s/381/382/\" \"\$2\", which BSD sed rejects; it fails every local push and fast tier on macOS and passes on Linux. jlevy/squares#254 replaces that test file with branch B version; check whether the replacement has the same fixture, and fix it there.
