---
type: is
id: is-01m2dz8pe5q7v6s8pkykp2qpg2
title: "T1 reader: bind every atom row and captured weight to reviewed source"
kind: bug
status: closed
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - bc303
  - admission
dependencies: []
parent_id: is-01m2b8wag8sa0p3mna22wmr3c6
hold: null
hold_until: null
created_at: 2026-09-13T18:07:57.380Z
updated_at: 2026-09-13T19:42:05.035Z
closed_at: 2026-09-13T19:42:05.034Z
close_reason: Isolated T1 reader repair 74ec773c passed 11 focused tests; independent Astra Max exact-head review accepted both source-row authentication and executing-reader provenance. It independently checked 377 source atoms, 17 retained-record mutations, and 10 provenance controls. No T1 campaign determination/global routing/new bound promoted; separate stacked PR remains think-uula.
resolution: null
duplicate_of: null
---
Independent Astra Max review at 88d54d85 accepted finite witness arithmetic but found validate_record/encode_record accept altered captured weights, a negative excluded weight, or excluded coordinates outside the parent under an unchanged source manifest. Reconstruct and compare every atom row and weight against source-bound input before publishing determination.
