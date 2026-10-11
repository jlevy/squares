---
type: is
id: is-01m18qcj9wm7n23db7hts1c20w
title: "agenda-008 block 4: change-scoped gate selection that cannot silently under-select"
kind: task
status: closed
priority: 1
version: 2
labels: []
dependencies: []
created_at: 2026-08-30T06:58:21.628Z
updated_at: 2026-10-06T08:42:15.710Z
closed_at: 2026-10-06T08:42:15.709Z
close_reason: "Done: agenda-008 BC-084 (bead think-9qtn) is state complete and the agenda is completed. The conservative change-scoped selector is devtools/reachable_tests.py (BC-086), errs toward inclusion with whole-suite fallbacks, and is held by tests/test_reachable_tests.py and test_change_scoped_selection.py."
resolution: null
duplicate_of: null
---
BC-051's work, unchanged in scope: map a changed path to the steps it can reach, conservative by construction, with a negative control proving it cannot under-select.
