---
type: is
id: is-01m49m1v8q316etk1g7kkr3hsq
title: "Lane: high-precision KKT re-solve + bounded integer-relation sweep for numeric-only counts"
kind: task
status: in_progress
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-10-06-exact-side-values.md
delegate: claude-code@vm
labels:
  - packing
dependencies: []
parent_id: is-01m49m0enx3qf7mm1kyrra0z10
hold: null
hold_until: null
created_at: 2026-10-06T22:06:24.535Z
updated_at: 2026-10-06T22:21:40.139Z
started_at: 2026-10-06T22:21:40.139Z
---
W6. Register H-NNN with frozen accept rule (relation verified at 2x the digits used to find it, irreducible, root isolates S_exact). Instrument wraps retained exactsolve.py (read before run) on Daniel's KKT points for the 54 numeric-only counts at rising precision; records identifications as contact-system with evidence, and negatives with degree/height/digit scope. Excludes n=29 (owned by think-je8y/obgk/gucc) and the 7 counts without a KKT point (105,130,292; bound-only 177,211,263,272).
