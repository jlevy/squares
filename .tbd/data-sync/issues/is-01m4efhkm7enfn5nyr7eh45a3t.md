---
type: is
id: is-01m4efhkm7enfn5nyr7eh45a3t
title: Remove redundant catalogue fixture reads identified in PR434 review
kind: chore
status: in_progress
priority: 4
version: 2
delegate: intake_remaining_fixes
labels: []
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-08T19:23:50.278Z
updated_at: 2026-10-08T22:39:28.978Z
started_at: 2026-10-08T22:39:28.977Z
---
Independent senior review of PR434 head637af4 identified Low A1: packing/tests/test_kingbird_catalogue.py repeats the same stateless _record_catalogue() and _kingbird_source_key() reads at lines391–392 after388–389 without an additional assertion. Deferred from the intake stack because it changes neither scientific evidence nor test coverage and would trigger unrelated stack validation. On the next focused catalogue-test maintenance change, delete only the redundant second pair, preserve every assertion and fixture value, and run the selected catalogue fixture tests. Keep this bead open until that correction is committed and validated.
