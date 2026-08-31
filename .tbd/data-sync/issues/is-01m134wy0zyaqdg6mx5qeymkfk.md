---
type: is
id: is-01m134wy0zyaqdg6mx5qeymkfk
title: "PR #50 review R7: Medium: ContactStructure under-specifies the discrete hypothesis"
kind: bug
status: closed
priority: 2
version: 2
labels:
  - packing
dependencies: []
parent_id: is-01m134wbw78hcnh0fsgqtej4rk
created_at: 2026-08-28T02:59:02.814Z
updated_at: 2026-08-28T03:20:04.120Z
closed_at: 2026-08-28T03:20:04.120Z
close_reason: "Addressed in a236598; disposition map posted to PR #50"
resolution: null
duplicate_of: null
---
impl spec:173-189,221. Incidence carries only pair/wall kind, indices, wall name, margin. It omits WHICH corner touches WHICH edge and the contact type (corner-edge vs edge-edge vs corner-corner). With 15 axis-aligned squares many of the 52 pair contacts are edge-edge, a different equation. ContactSystem shape and the centre-elimination map are unspecified.
