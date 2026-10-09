---
type: is
id: is-01m4efhkm7enfn5nyr7eh45a3t
title: Remove redundant catalogue fixture reads identified in PR434 review
kind: chore
status: closed
priority: 4
version: 3
delegate: intake_remaining_fixes
labels: []
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-08T19:23:50.278Z
updated_at: 2026-10-09T01:34:34.119Z
started_at: 2026-10-08T22:39:28.977Z
closed_at: 2026-10-09T01:34:34.117Z
close_reason: "Fixed in source commit e0792f403b8c47a68a7f4f34e4936155a2acf60f: deleted only the redundant second _record_catalogue() and _kingbird_source_key() pair, preserving every fixture byte and assertion. The focused catalogue check passed; exact-head PR434 at abb822fb8788ca187a25a97ff465996c033b5475 passed actual required Packing run37864114853, Pages run37864114912 and full checkpoint37864151667 including all twelve scientific/integration jobs and aggregate. ROOT merged PR434 as b810432cccf7849920dda3aad76882f191464eb5; its tree exactly equals the qualified branch. Fixed A1 disposition is published at https://github.com/jlevy/squares/pull/434#issuecomment-6071168740. No new tests were rerun for this bookkeeping closure; broad frontend bead think-5jr5 remains open."
resolution: null
duplicate_of: null
---
Independent senior review of PR434 head637af4 identified Low A1: packing/tests/test_kingbird_catalogue.py repeats the same stateless _record_catalogue() and _kingbird_source_key() reads at lines391–392 after388–389 without an additional assertion. Deferred from the intake stack because it changes neither scientific evidence nor test coverage and would trigger unrelated stack validation. On the next focused catalogue-test maintenance change, delete only the redundant second pair, preserve every assertion and fixture value, and run the selected catalogue fixture tests. Keep this bead open until that correction is committed and validated.
