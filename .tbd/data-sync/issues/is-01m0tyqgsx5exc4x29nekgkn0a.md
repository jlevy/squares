---
type: is
id: is-01m0tyqgsx5exc4x29nekgkn0a
title: Separate traceability, reproducibility, numerical evidence, and formal certification
kind: task
status: in_progress
priority: 1
version: 11
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-frontier-assurance-and-verification.md
labels:
  - packing
  - documentation
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
updated_at: 2026-08-25T04:09:05.726Z
---
Implement the two-axis frontier assurance contract. Preserve reported upper and lower claims separately from verified upper and lower bounds. Verified always requires exact formal evidence, while origin and independence distinguish a complete published proof or external certificate from a repository replay or audit. Keep assurance, method, actor, relationship to generator, actual precision, tolerance, formal artifact, replay, and blocker independent. Add the v2 case, evidence, experiment, witness, and document-map contracts with semantic checks where softschema cannot express cross-field rules. A mere citation stays reported; a local audit adds evidence rather than rewriting provenance.

## Notes

2026-08-24: implementation begins on stacked branch codex/packing-frontier-contract from PR #26 head 3d299d5. Red-green order: characterize v1 acceptance and required v2 rejections; add structural schemas and cross-record semantic checks; migrate current records only after the validator fails for the intended reasons.
