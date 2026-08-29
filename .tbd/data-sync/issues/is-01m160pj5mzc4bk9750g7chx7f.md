---
type: is
id: is-01m160pj5mzc4bk9750g7chx7f
title: "Block 7: chirality in the pose model"
kind: task
status: closed
priority: 1
version: 2
labels: []
dependencies: []
created_at: 2026-08-29T05:43:23.060Z
updated_at: 2026-08-29T06:34:26.015Z
closed_at: 2026-08-29T06:34:26.015Z
close_reason: "Closed in session-040. The corner model now carries a per-square chirality: corner_k = c + R(t).(sigma*ox_k/2, oy_k/2). The n=29 assembled residual falls from 2.0 to 1.3e-15 across 94 equations; the n=11 calibration is unmoved at 4.4e-16, rank 30, shortfall 4. The feature-renaming cost this bead was written to weigh was not paid — reflecting the local axis leaves corner indices alone. Assembled n=29 system: rank 81 of 88, shortfall 7, with a null space that moves 26 squares at constant side."
resolution: null
duplicate_of: null
---
agenda-006 BC-059. Seven n=29 squares are reflected and a centre-plus-rotation pose cannot represent them. Give the pose a chirality so reflected layouts assemble, or state what that costs the feature naming.
