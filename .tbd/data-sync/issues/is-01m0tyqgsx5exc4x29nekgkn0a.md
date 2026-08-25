---
type: is
id: is-01m0tyqgsx5exc4x29nekgkn0a
title: Separate traceability, reproducibility, numerical evidence, and formal certification
kind: task
status: closed
priority: 1
version: 13
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
updated_at: 2026-08-25T07:24:21.144Z
closed_at: 2026-08-25T07:24:21.144Z
close_reason: The definitive docs and v2 contracts now reserve verified for formal evidence, use numerically checked for numerical work, retire polished and ambiguous arbitrary-precision labels, and define campaign/session/series/experiment/round/run consistently.
resolution: null
duplicate_of: null
---
Implement the two-axis frontier assurance contract. Preserve reported upper and lower claims separately from verified upper and lower bounds. Verified always requires exact formal evidence, while origin and independence distinguish a complete published proof or external certificate from a repository replay or audit. Keep assurance, method, actor, relationship to generator, actual precision, tolerance, formal artifact, replay, and blocker independent. Add the v2 case, evidence, experiment, witness, and document-map contracts with semantic checks where softschema cannot express cross-field rules. A mere citation stays reported; a local audit adds evidence rather than rewriting provenance.

## Notes

Simplified FrontierEvidence/v1 authoring by omitting method-specific null placeholders (161 removed) while retaining consumed classification/replay fields. Added strict duplicate-YAML-key loading after finding an overwritten evidence field pattern; witness and frontier schema gates now reject ambiguity. Focused assurance/witness tests and 100 frontmatter + 13 pure-YAML validation pass.
