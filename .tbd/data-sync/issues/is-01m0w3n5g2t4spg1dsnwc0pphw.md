---
type: is
id: is-01m0w3n5g2t4spg1dsnwc0pphw
title: Freeze the n4 fixture receipt outside fixture data
kind: bug
status: closed
priority: 1
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - packing
  - validity
  - testing
dependencies: []
parent_id: is-01m0tyazcycsqvm34fyxb4hdtx
created_at: 2026-08-25T09:22:38.721Z
updated_at: 2026-08-25T09:26:46.632Z
closed_at: 2026-08-25T09:26:46.631Z
close_reason: "D-261 fixed: test code independently freezes success=false, status=4, and the exact HiGHS message; only a finite successful nine-variable solve with every original-row residual <=1e-10 is the portable alternative."
resolution: null
duplicate_of: null
---
The first replay test treated whatever status/success/message the YAML declared as its expected failure, so coordinated drift in the fixture could redefine the acceptance rule. Hard-code the only accepted failure as HiGHS status 4 with success false and the retained message; otherwise accept only a successful solution whose complete original-row replay is <=1e-10.
