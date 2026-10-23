---
type: is
id: is-01m5kcwt9g3d788pr4actc49ah
title: Replace brittle site copy and corpus assertions with independent semantic contracts
kind: task
status: in_progress
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md
delegate: followups-coordinator
labels: []
dependencies: []
parent_id: is-01m5kcfhfdmgfb03gn3drg43rc
hold: null
hold_until: null
created_at: 2026-10-23T03:29:25.794Z
updated_at: 2026-10-23T04:15:52.807Z
started_at: 2026-10-23T03:45:46.708Z
---
Delegated Astra audit: overview exact invitations/lead-ins/full sentences/markup at tests/test_overview.py lines7484-7525 and4289-4317 should assert parsed nonempty introduction, formal identity and canonical destinations. Filter expected shown_by_default/count_text/landed_day mirrors production and live T122/T003: use tiny independent cutoff/date/supersession fixtures plus real-registry wiring. Homepage lines702-754 duplicates ordering/count9/PAPER[-2:]: assign one semantic owner and retain browser alignment/navigation. Contributor lines42-126: parse hrefs/Sources instead of string locks; preserve unsafe-URI refusal, provenance and no invented identity. Tests must reject missing content, wrong links and boundary off-by-one errors while passing copy edits and corpus growth. Verify exact paths before edits; no implementation during PR737 landing.

## Notes

PR743 removed obsolete profile-overlay browser tests, replaced exact introduction-copy assertions with semantic presence checks, and retained native navigation, focus/race and unsafe-source coverage. Remaining work: independent small filter-boundary fixtures and broader homepage/contributor corpus/string assertion cleanup from original audit. Keep open; not a blocker for requested tutorial/design fixes.
