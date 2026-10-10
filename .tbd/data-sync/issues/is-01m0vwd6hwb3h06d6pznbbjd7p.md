---
type: is
id: is-01m0vwd6hwb3h06d6pznbbjd7p
title: Adapt PR 26 to the W7 taxonomy and current validation entry points
kind: task
status: closed
priority: 0
version: 6
spec_path: docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - packing
  - upstream
dependencies: []
parent_id: is-01m0vrwg66tynnceae6y3p932y
created_at: 2026-08-25T07:15:57.612Z
updated_at: 2026-10-10T22:49:23.774Z
closed_at: 2026-10-06T08:29:58.236Z
close_reason: |
  Done (bead review 2026-10-06, origin/main eb43ffe9a): PR #26 MERGED 2026-08-25 (adapted and merged by the upstream agent that owned its head)
resolution: null
duplicate_of: null
---
Before PR 26 merges, port its frontier-assurance plan onto post-PR28 main: replace the stale six-workflow/general-improvement framing with W1-W7 and W7 pipeline-improvement, replace removed tools/test.sh commands with current module and packing-validate entry points, update think-wfz1 provenance, run focused documentation checks plus the normal gate, update the PR receipt, and merge.

## Notes

Parallel upstream agent owns the live PR 26 head. Root preserved a local unpushed adaptation stash and will not duplicate or push over that work; verify the live head instead.
