---
type: is
id: is-01m5kcwtsppq1865v3nrmqj0sk
title: Align release iteration instructions and base-movement monitoring with hosted parallel gates
kind: task
status: closed
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md
delegate: followups-coordinator
labels: []
dependencies: []
parent_id: is-01m5kcfhfdmgfb03gn3drg43rc
hold: null
hold_until: null
created_at: 2026-10-23T03:29:26.325Z
updated_at: 2026-10-23T04:12:20.965Z
started_at: 2026-10-23T03:45:46.716Z
closed_at: 2026-10-23T04:12:20.965Z
close_reason: "Implemented in PR743: removed unused Recent Results pipeline/Atlas table script and documented focused-checks then hosted validation with concurrent review and mergeability monitoring."
resolution: null
duplicate_of: null
---
Owner workflow is focused local checks then push, full hosted gates in parallel with review. Reconcile development.md around line226 full-local wording with this rule and #724 while retaining explicit research/checkpoint obligations and current-head required checks. Branch mergeability workflow currently reacts to pushes and can miss base movement during waiting: investigate refresh/monitoring against changed base with bounded evidence, avoiding repeated full local gates. Preserve merge provenance and substantive validation. Document proposed change before implementation; PR737 delivery proceeds independently.
