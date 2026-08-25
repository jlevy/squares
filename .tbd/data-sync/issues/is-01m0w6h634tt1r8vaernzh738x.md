---
type: is
id: is-01m0w6h634tt1r8vaernzh738x
title: Correct stale deleted paths and formatting in the delegated promotion check
kind: bug
status: closed
priority: 2
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - packing
  - bookkeeping
dependencies: []
parent_id: is-01m0w6ccwc89mjnmtvnk1xa2qh
created_at: 2026-08-25T10:12:53.988Z
updated_at: 2026-08-25T10:17:42.690Z
closed_at: 2026-08-25T10:17:42.690Z
close_reason: "D-271, D-273, and D-274 are recorded and fixed before integration: the phase transition uses the enforced enum, the workflow test proves a single exact blocking command with no advisory escape, and corrected focused checks plus the complete gate pass."
resolution: null
duplicate_of: null
---
The first delegated Ruff command named the two classifier files after deleting them and found the new module-boundary assertion unformatted/E501 at line 215. Remove deleted paths from the command, format the assertion, record the receipt, and require the corrected focused format/lint/test commands before integration.
