---
type: is
id: is-01m0nym15cp58q045s10cb3awb
title: Algebraic scalar over Q(alpha), FLINT-backed
kind: task
status: open
priority: 1
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md
labels: []
dependencies: []
parent_id: is-01m0p5tswc9s27gb5c1d3da27b
created_at: 2026-08-22T23:59:12.044Z
updated_at: 2026-08-23T05:26:45.402Z
---
Exact zero test and exact sign. FLINT rather than hand-rolled: measured 177x over pure Python at degree 8 and 578x at degree 62, and the record table reaches 62. Open question in the spec: flint-sys vs rug vs malachite -- measure, do not assume.
