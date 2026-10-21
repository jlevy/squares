---
type: is
id: is-01m5frh64q04x1zngbk2cmxx1q
title: Show years active from reviewed original work
kind: task
status: closed
priority: 2
version: 5
delegate: profiles_data_integration
labels: []
dependencies: []
parent_id: is-01m5fpv2yk09g6z1a17rts4wzc
hold: null
hold_until: null
created_at: 2026-10-21T17:35:49.910Z
updated_at: 2026-10-21T21:45:33.735Z
started_at: 2026-10-21T17:35:55.878Z
closed_at: 2026-10-21T21:45:33.735Z
close_reason: Completed bounded implementation, reviewed evidence and local/hosted feature acceptance. Final-head CI and separate runtime/evidence followups remain open.
resolution: null
duplicate_of: null
---
Show Years active in the directory and individual profiles from reviewed original authorship/publication years and explicitly dated own contributions. Never extend activity using later reuse, citation/import/registration dates or another finder date. Use one year or an en-dash range and leave unsupported activity blank. Historical contribution-event schema gaps remain separately tracked by think-0ltn.

## Notes

Pure years_active helper implemented and tested. UI mapping must use reviewed published/established dates only; no registered/import fallback for activity. Single year, range, or unspecified. Integrated render checks pending.

Completed the corrected original-work activity model and directory/profile presentation. person_activity_years uses reviewed original author/publication evidence, explicitly dated own support/finder/prover contributions and first-party established dates; later reuse, citation years, import/registration dates and undated improver activity cannot extend the range. Source-specific years remain independent of compound result publication dates. Single years and en-dash ranges render correctly; sparse/unknown evidence remains blank. This supersedes the original broad credited-result-date description and is the resolved behavior of think-gjxb. The live historical regression includes Stromquist 2003 without spurious 2026 reuse, partial-date validation and the audited profile subset; the post-adoption identity/tally/coverage selection passed 54 tests in 8.47 seconds. Historical dated-contribution modeling remains separately open under think-0ltn.

Final integration evidence: the scoped work is committed and published in https://github.com/jlevy/squares/pull/578, currently at db3cb6d4fe5f00a44d04a8ef91018aa2b365bad8. Hosted validation at e162a870a899a61cc77cd47fa2f56c0ff388c8ea passed Pages, Packing Validate and suites B/C; suite A passed all 4,364 assertion tests, then failed only the separate project-tally CALL wall guard. That independent runtime defect is fixed in e3e33171bf1d687190cc957a40e25fbbc9dbb23c and remains tracked by think-rolz while final-head CI runs. The exact final db3 CI verdict is not claimed here. This closure is for completed bounded acceptance; the overall think-zpfo handoff, think-uwd6 coverage parent, historical registrations, pending PDF census and real evidence gaps remain open.
