---
type: is
id: is-01m134wy0zyaqdg6mx5qeymkfk
title: "PR #50 review R7: Medium: ContactStructure under-specifies the discrete hypothesis"
kind: bug
status: open
priority: 2
version: 1
labels:
  - packing
dependencies: []
parent_id: is-01m134wbw78hcnh0fsgqtej4rk
created_at: 2026-08-28T02:59:02.814Z
updated_at: 2026-08-28T02:59:02.814Z
---
impl spec:173-189,221. Incidence carries only pair/wall kind, indices, wall name, margin. It omits WHICH corner touches WHICH edge and the contact type (corner-edge vs edge-edge vs corner-corner). With 15 axis-aligned squares many of the 52 pair contacts are edge-edge, a different equation. ContactSystem shape and the centre-elimination map are unspecified.
