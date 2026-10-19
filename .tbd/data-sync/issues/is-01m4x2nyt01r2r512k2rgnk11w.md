---
type: is
id: is-01m4x2nyt01r2r512k2rgnk11w
title: n-029.md prints a verified upper bound 5.43e-20 above its own exact form
kind: bug
status: in_progress
priority: 2
version: 2
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-14T11:27:37.791Z
updated_at: 2026-10-18T08:50:25.696Z
started_at: 2026-10-18T08:50:25.695Z
---
Found by the PR #574 intake lane (think-9v2k) on 2026-10-14: packing/frontier/n-029.md prints a verified value 5.43e-20 above the exact form the same record states, so the printed verified side and its exact form disagree. Check which is right against the house's certificate, fix the record through its writer (not by hand), and add a check that a case record's printed verified side rounds its exact form in the declared direction. Branch with the finding: claude/wizardly-meitner-wqn4x3-intake-1014-pr574 @ 56cf868c6.
