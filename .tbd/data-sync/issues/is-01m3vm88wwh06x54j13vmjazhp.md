---
type: is
id: is-01m3vm88wwh06x54j13vmjazhp
title: Independently implement and review the H255 root-certificate checker
kind: task
status: closed
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-10-01-post-optimality-w3-session.md
labels: []
dependencies: []
parent_id: is-01m3vkftza0gk08jwefckcgfmr
created_at: 2026-10-01T11:40:33.051Z
updated_at: 2026-10-01T11:56:11.780Z
closed_at: 2026-10-01T11:56:11.780Z
close_reason: Independent exact root producer/checker completed,13 synthetic controls pass and Astra max approves; frozen b3e5e1526. H255 run outputs under separate review.
resolution: null
duplicate_of: null
---
Astra max independently implements the polynomial root-certificate checker without reading/importing producer arithmetic or acceptance. Recompute fixed coefficients, derivatives, intervalJacobian, inverse, contraction/inclusion and source/domain guards; reject tamperedfields and malformeddata. Separate Astra reviewer audits both. Same mathematical method, not method-diverse confirmation.
