---
type: is
id: is-01m0vj2kggw0dc6xrnnvys7f93
title: "PR #23 review R8: Turn the macOS deep diagnostic into an asserted known outcome"
kind: bug
status: closed
priority: 2
version: 3
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-packing-engineering-maturity.md
delegate: codex@spud10
labels:
  - engineering-maturity
  - pr-review
  - pr-23
dependencies: []
parent_id: is-01m0vj13yefxcxhhew81ewfpvq
hold: null
hold_until: null
created_at: 2026-08-25T04:15:24.687Z
updated_at: 2026-08-25T04:44:37.664Z
started_at: 2026-08-25T04:16:15.495Z
closed_at: 2026-08-25T04:44:37.663Z
close_reason: "Completed in 69e65eb: macOS CI now asserts D-203's exact known n=4 drift and fails on an unexpected pass or any different failure; local Python 3.14.7 probe passed."
resolution: null
duplicate_of: null
---
PR 23 review R8. File: .github/workflows/packing-validation.yml lines 78-86. Replace unconditional continue-on-error with a check that passes only for the recorded D-203 failure and alarms on pass or a different failure.
