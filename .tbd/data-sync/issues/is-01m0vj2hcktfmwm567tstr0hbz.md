---
type: is
id: is-01m0vj2hcktfmwm567tstr0hbz
title: "PR #23 review R3: Distinguish missing provenance objects from orphaned commits"
kind: bug
status: in_progress
priority: 2
version: 2
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
created_at: 2026-08-25T04:15:22.514Z
updated_at: 2026-08-25T04:16:15.453Z
started_at: 2026-08-25T04:16:15.453Z
---
PR 23 review R3. File: explorations/packing/src/sqpack/cli/validate.py lines 543-579. Detect whether each recorded commit object exists before ancestry checks and give a shallow-clone remediation instead of blaming the artifact.
