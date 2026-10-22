---
type: is
id: is-01m5jczh01a1tdr0x7h4dc686j
title: Order shared cards and profile work as Records Results Credits
kind: task
status: closed
priority: 2
version: 5
spec_path: docs/project/specs/active/plan-2026-10-10-contributor-profiles.md
delegate: squaremath-tally-order
labels: []
dependencies: []
parent_id: is-01m5jct23n8s7fj3ydf94n0yhv
hold: null
hold_until: null
created_at: 2026-10-22T18:11:40.159Z
updated_at: 2026-10-22T18:19:48.660Z
started_at: 2026-10-22T18:11:53.399Z
closed_at: 2026-10-22T18:17:36.145Z
close_reason: Delegated tally-order implementation and targeted regressions complete; 3 ordering tests and 59 full focused tests pass. Coordinator owns final shared-file validation, commit, and PR.
resolution: null
duplicate_of: null
---
Implement the delegated tally/section ordering portion of the user follow-up: use Records, then Results, then Credits in shared project/resource cards, per-profile tally summaries, and profile work sections. Directory summaries and table columns already use that order and must remain correct. Preserve exact counts, significance formatting, hyperlinks, blank/zero rules, and pending-comparison semantics.

Write ownership: overview_sections.project_tally; render_contributors.profile_tally and _credited_work; corresponding targeted tests. Coordinator separately owns naming functions and documentation in shared files. No commit or push.

## Notes

Implemented Records, Results, Credits order in overview_sections.project_tally, render_contributors.profile_tally, and _credited_work sections. Directory summary/table were already correct and remain unchanged. Reused the existing register/occurrence test fixtures to assert counts/significance markup, exact profile links, current-plus-pending and pending-only messages, section order, and known-zero text. Updated only the actual resource-card expected ordering in the coordinator-shared test file. Red baseline: 3 failed, 40 deselected in 39.54s. Green targeted: 3 passed, 40 deselected in 31.05s. Full focused profile/record-presentation/tally files: 59 passed in 18.88s. BasedPyright for two source/two test files: 0 errors, 0 warnings, 0 notes. No commit or push; coordinator owns final integration and publication.
