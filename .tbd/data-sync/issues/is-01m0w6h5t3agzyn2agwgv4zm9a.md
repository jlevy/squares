---
type: is
id: is-01m0w6h5t3agzyn2agwgv4zm9a
title: Strengthen the direct-blocking macOS workflow contract
kind: bug
status: closed
priority: 1
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - packing
  - validity
  - review
dependencies: []
parent_id: is-01m0w6ccwc89mjnmtvnk1xa2qh
created_at: 2026-08-25T10:12:53.698Z
updated_at: 2026-08-25T10:17:42.683Z
closed_at: 2026-08-25T10:17:42.683Z
close_reason: "D-271, D-273, and D-274 are recorded and fixed before integration: the phase transition uses the enforced enum, the workflow test proves a single exact blocking command with no advisory escape, and corrected focused checks plus the complete gate pass."
resolution: null
duplicate_of: null
---
Independent phase-13 review found the draft workflow test would still pass with a second obsolete wrapper step, shell-masked success such as || true, or job-level continue-on-error. Require exactly one focused-deep step, exact normalized command equality, no job/step continue-on-error, and absence of the old wrapper across every macOS run command.
