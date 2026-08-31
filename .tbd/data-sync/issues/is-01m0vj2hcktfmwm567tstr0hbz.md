---
type: is
id: is-01m0vj2hcktfmwm567tstr0hbz
title: "PR #23 review R3: Distinguish missing provenance objects from orphaned commits"
kind: bug
status: closed
priority: 2
version: 6
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
updated_at: 2026-08-25T04:52:33.841Z
started_at: 2026-08-25T04:16:15.453Z
closed_at: 2026-08-25T04:52:33.839Z
close_reason: "Completed in 9736b10 after CI validation: provenance distinguishes reachable, orphaned, and missing objects; a missing object passes only when the artifact explicitly names that commit as unreachable historical loss, rendering UNAVAILABLE, while unannotated missing objects still fail with fetch remediation. Full 31-step gate passed in 102.35s with 34 pytest contracts."
resolution: null
duplicate_of: null
---
PR 23 review R3. File: explorations/packing/src/sqpack/cli/validate.py lines 543-579. Detect whether each recorded commit object exists before ancestry checks and give a shallow-clone remediation instead of blaming the artifact.

## Notes

Reopened: CI on 69e65eb showed that the deliberately lost exp-001 commit is absent even after fetch-depth 0; refine R3 so annotated historical loss is reported as unavailable while unannotated missing objects still fail with fetch remediation.
