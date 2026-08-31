---
type: is
id: is-01m0trxw9xh8q7tjnte4zjbk7d
title: Fix tied-support conjunctions in n=5 tangent cones
kind: bug
status: closed
priority: 1
version: 4
spec_path: explorations/packing/campaign/agendas/agenda-001-basin-confidence-ladder.md
labels:
  - packing
  - soundness
  - experiment-tooling
dependencies: []
parent_id: is-01m0tpn9ej3z97jr6nq97fb9gt
created_at: 2026-08-24T20:55:55.439Z
updated_at: 2026-08-24T21:17:58.997Z
closed_at: 2026-08-24T21:17:58.995Z
close_reason: "Fixed in aa63cf4 and executed in exp-035: pair (3,4) has two owner-axis branches with both tied support rows retained in each; the coherent missing-row mutation rejects. Frozen generation and replay both passed."
resolution: null
duplicate_of: null
---
The unexecuted candidate checker treats the two tied support derivatives for pair (3,4) as alternative SAT branches. For a fixed owner axis the support function is a maximum, so both one-sided support inequalities must hold; only the owner-axis choice is a disjunction. Derive this structure exactly, retain two owner branches with both feature rows, add a mutation that drops one tied row, and log as D-195 before exp-035.

## Notes

2026-08-24 correction checkpoint: pair (3,4) is now represented by exactly two owner-axis branches. Each owner branch retains both tied support-feature derivative rows as simultaneous inequalities. The record carries the full matrices and a mutation deletes one tied row while coherently changing redundant counts/digest; validation rejects it. Static-only validation is green; target execution remains prohibited until exp-035 is preregistered.
