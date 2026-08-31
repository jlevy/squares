---
type: is
id: is-01m0w39mwjkzcb2adpv4e8ge3r
title: Prevent cross-wired n4 solver fixture context
kind: bug
status: closed
priority: 1
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - packing
  - validity
  - measurement
dependencies: []
parent_id: is-01m0tyazcycsqvm34fyxb4hdtx
created_at: 2026-08-25T09:16:21.265Z
updated_at: 2026-08-25T09:26:46.368Z
closed_at: 2026-08-25T09:26:46.367Z
close_reason: "D-260 fixed before persistence: discarded the cross-wired capture; retained same-call theta/cell and solver arrays; independent 22-row/22-RHS exact rebuild and a mutated first-axis control now guard the fixture."
resolution: null
duplicate_of: null
---
The first delegated seed-0 capture paired the failing A_ub/b_ub with theta and a separating cell from another fixed-point evaluation. The mismatch was caught before persistence because rebuilding the LP from the stored context did not equal the retained matrix. Record D-260, discard the artifact, recapture theta/cell and linprog inputs from the same solve_cell invocation, and require exact rebuild equality plus a structural mutation control before any fixture can pass.
