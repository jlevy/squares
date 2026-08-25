---
type: is
id: is-01m0vj2pg056qp8x4vp1s92vb4
title: "PR #23 review R16: Make basin-event replay coverage discover new archives"
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
created_at: 2026-08-25T04:15:27.744Z
updated_at: 2026-08-25T04:44:40.490Z
started_at: 2026-08-25T04:16:15.544Z
closed_at: 2026-08-25T04:44:40.490Z
close_reason: "Completed in 69e65eb: basin-event replay archives are discovered by their versioned contract; all 14 v2/v3 journals now replay, including exp-019 and exp-020."
resolution: null
duplicate_of: null
---
PR 23 review R16. File: explorations/packing/src/sqpack/cli/validate.py lines 223-236. Derive replay inputs from the authoritative result registry or assert that every replayable archive is listed.
