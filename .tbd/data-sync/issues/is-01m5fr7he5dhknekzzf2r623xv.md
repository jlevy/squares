---
type: is
id: is-01m5fr7he5dhknekzzf2r623xv
title: Link credit evidence to GitHub issues and pull requests
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
created_at: 2026-10-21T17:30:33.796Z
updated_at: 2026-10-21T21:45:33.730Z
started_at: 2026-10-21T17:30:43.351Z
closed_at: 2026-10-21T21:45:33.730Z
close_reason: Completed bounded implementation, reviewed evidence and local/hosted feature acceptance. Final-head CI and separate runtime/evidence followups remain open.
resolution: null
duplicate_of: null
---
Where existing credit/contribution evidence has GitHub issue or PR URLs, render navigable number references with canonical GitHub issue and pull-request branch icons; share component, preserve repository context/accessibility, do not infer unsupported references.

## Notes

Safe exact GitHub issue/PR URL parser, dedupe, typed Octicons and explicit source/registration/supporting evidence joins implemented. Shared helper suites: 37 passed; Ruff and BasedPyright clean; Astra read-only helper review found no blockers. Renderer integration remains in progress.

Completed renderer integration: contribution_references uses the shared exact GitHub URL parser and canonical issue/PR Octicons, preserving safe comment targets, deduplicated references, number labels and repository/type accessibility. The visible groups distinguish Source, Registered in and Supporting evidence; registering PRs do not imply authorship by the credited person. Source-coverage/changelog inputs are declared build dependencies. Existing 37 helper tests passed with clean Ruff/BasedPyright and Astra review; the completed renderer and browser integration is covered by the hosted behavioral acceptance below.

Final integration evidence: the scoped work is committed and published in https://github.com/jlevy/squares/pull/578, currently at db3cb6d4fe5f00a44d04a8ef91018aa2b365bad8. Hosted validation at e162a870a899a61cc77cd47fa2f56c0ff388c8ea passed Pages, Packing Validate and suites B/C; suite A passed all 4,364 assertion tests, then failed only the separate project-tally CALL wall guard. That independent runtime defect is fixed in e3e33171bf1d687190cc957a40e25fbbc9dbb23c and remains tracked by think-rolz while final-head CI runs. The exact final db3 CI verdict is not claimed here. This closure is for completed bounded acceptance; the overall think-zpfo handoff, think-uwd6 coverage parent, historical registrations, pending PDF census and real evidence gaps remain open.
