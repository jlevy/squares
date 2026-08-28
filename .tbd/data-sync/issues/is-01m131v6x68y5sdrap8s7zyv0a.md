---
type: is
id: is-01m131v6x68y5sdrap8s7zyv0a
title: Solve the closed contact system exactly, by elimination or integer relation
kind: feature
status: open
priority: 1
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-28-numeric-symbolic-round-trip.md
labels:
  - packing
dependencies: []
parent_id: is-01m0tyy5k7e4ags20c1fxqth7f
created_at: 2026-08-28T02:05:40.645Z
updated_at: 2026-08-28T02:26:38.756Z
---
Step 5 of the symbolic promotion route, unbuilt. No Groebner, resultant, PSLQ or LLL code exists in the tree; SymPy appears in three files and none is a general solver.

Two routes: elimination (Groebner basis in lex order, or resultants), or high-precision Newton followed by an integer relation algorithm that recognises the minimal polynomial.

Both produce guesses and both must be discharged. Integer relation finds a relation, not a proof: a degree-8 relation holding to 500 digits is overwhelming evidence and zero proof. Irreducibility over Q must be checked, the intended real root isolated from the others, and the result substituted back exactly. sqpack.field already does that half soundly, which is why step 6 is where this repository is strong.

Blocked on the contact system existing.
