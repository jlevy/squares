---
type: is
id: is-01m0vj2maxdy8v317hcne60rry
title: "PR #23 review R11: Delete the unreachable strict-without-deep guard"
kind: bug
status: closed
priority: 3
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
created_at: 2026-08-25T04:15:25.532Z
updated_at: 2026-08-25T04:44:38.480Z
started_at: 2026-08-25T04:16:15.511Z
closed_at: 2026-08-25T04:44:38.479Z
close_reason: "Completed in 69e65eb: the unreachable strict-without-deep production guard was removed and its mutation protection moved to a focused orchestration contract."
resolution: null
duplicate_of: null
---
PR 23 review R11. File: explorations/packing/src/sqpack/cli/validate.py around line 827. Remove the branch that cannot be reached because strict always enables deep.
