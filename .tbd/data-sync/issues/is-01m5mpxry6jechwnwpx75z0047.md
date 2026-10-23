---
type: is
id: is-01m5mpxry6jechwnwpx75z0047
title: "PR #748 A4: importing state_ai_assistance fails on a bad anchor despite load_statements' guarantee"
kind: bug
status: closed
priority: 2
version: 3
delegate: c-gates-1023
labels: []
dependencies: []
parent_id: is-01m5mpx469084wmghw63k1vasv
hold: null
hold_until: null
created_at: 2026-10-23T15:43:57.381Z
updated_at: 2026-10-23T16:50:18.138Z
started_at: 2026-10-23T15:44:49.947Z
closed_at: 2026-10-23T16:50:18.137Z
close_reason: "Fixed in 9ed29dc26: wand125() resolved lazily, statement_of raises LookupError; test_a_bad_anchor_is_reported_by_check_and_breaks_no_import. Disposition https://github.com/jlevy/squares/pull/748#issuecomment-6370073707."
resolution: null
duplicate_of: null
---
packing/devtools/state_ai_assistance.py:153 WAND125 = statement_of(...) at import. Severity Low. Review A of PR #748: https://github.com/jlevy/squares/pull/748#issuecomment-6368647934.
