---
type: is
id: is-01m0wbd5hmx4q8gc0b4y3dps14
title: Bind H-042 branches to the retained exp-013 universe
kind: bug
status: open
priority: 1
version: 1
spec_path: explorations/packing/campaign/hypotheses/H-042-trump-incidence-rigidity-cores.md
labels:
  - packing
  - focus-correctness
dependencies: []
parent_id: is-01m0sg2venckvcs3q1cr5v1qzc
created_at: 2026-08-25T11:38:05.232Z
updated_at: 2026-08-25T11:38:05.232Z
---
Independent order-10 audit found derive_branch compares grouped rows only to a matrix key regenerated in the same call. It does not fail closed on the expected 128 matrices, 512 raw selections, active tables, or retained exp-013 branch record. Before expansion, assert the complete universe and replay a durable exp-013 binding for each selected matrix. D-292 owns this provenance boundary.
