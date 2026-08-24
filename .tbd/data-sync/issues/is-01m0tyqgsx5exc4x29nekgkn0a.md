---
type: is
id: is-01m0tyqgsx5exc4x29nekgkn0a
title: Separate traceability, reproducibility, numerical evidence, and formal certification
kind: task
status: open
priority: 1
version: 8
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-frontier-assurance-and-verification.md
labels:
  - packing
  - documentation
  - focus-process
dependencies:
  - type: blocks
    target: is-01m0tyqhyhcvcvh5e9j8p2ps0y
  - type: blocks
    target: is-01m0tyqj7srczg0jvc4za541dw
  - type: blocks
    target: is-01m0tz96g5svy9h1j9ntejmze9
  - type: blocks
    target: is-01m0v06qf4hksmdqc2rga0vr4x
parent_id: is-01m0typjn7s866m042zsemybj6
created_at: 2026-08-24T22:37:18.524Z
updated_at: 2026-08-24T23:04:03.976Z
---
Implement the multidimensional assurance contract from the frontier-assurance spec. Separate reported best from certified upper bound, and separate assurance, arithmetic or proof method, actor, independence, actual precision, tolerance, formal artifact, replay, and blocker. Migrate SquarePackingCase and Experiment schemas and add FrontierEvidence, Witness, and DocumentMap contracts. Schemas, tables, hashes, and logs never create mathematical rigor; each field and layer must name the failure it catches and claims it permits.
