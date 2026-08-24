---
type: is
id: is-01m0v06yyh15pkz846vsgxj1wc
title: Discharge the generic algebraic verifier's field preconditions
kind: bug
status: open
priority: 1
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-frontier-assurance-and-verification.md
labels:
  - packing
  - correctness
  - focus-correctness
dependencies:
  - type: blocks
    target: is-01m0tyy5k7e4ags20c1fxqth7f
parent_id: is-01m0typjn7s866m042zsemybj6
created_at: 2026-08-24T23:03:13.105Z
updated_at: 2026-08-24T23:04:03.660Z
---
The generic NumberField verifier can make exact sign decisions only after its defining polynomial is proved irreducible and its chosen real root is uniquely isolated, but the constructor does not enforce those preconditions. Preserve the sound built-in Trump path and make arbitrary algebraic inputs fail closed until they carry independently checked field metadata. Emit a replayable certificate for accepted inputs and negative controls for reducible polynomials and ambiguous root intervals. Acceptance: no generic caller can obtain assurance=verified without discharged field assumptions; rational degree-one inputs remain simple; the synopsis capability map and D-053 status match the implementation.
