---
type: is
id: is-01m2dz8pe5q7v6s8pkykp2qpg2
title: "T1 reader: bind every atom row and captured weight to reviewed source"
kind: bug
status: open
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - bc303
  - admission
dependencies: []
parent_id: is-01m2b8wag8sa0p3mna22wmr3c6
hold: blocked
hold_until: null
created_at: 2026-09-13T18:07:57.380Z
updated_at: 2026-09-13T18:13:47.325Z
---
Independent Astra Max review at 88d54d85 accepted finite witness arithmetic but found validate_record/encode_record accept altered captured weights, a negative excluded weight, or excluded coordinates outside the parent under an unchanged source manifest. Reconstruct and compare every atom row and weight against source-bound input before publishing determination.
