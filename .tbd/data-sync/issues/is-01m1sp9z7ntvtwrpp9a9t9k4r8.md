---
type: is
id: is-01m1sp9z7ntvtwrpp9a9t9k4r8
title: Formalize the adaptive witness-core theorem
kind: task
status: in_progress
priority: 1
version: 6
delegate: claude-code@spud10.local
labels:
  - research
dependencies:
  - type: blocks
    target: is-01m1sp9zj6d22raz1fyk1ervzw
  - type: blocks
    target: is-01m1spa0htnwp1s66yw18hxbv3
  - type: blocks
    target: is-01m1sp9x74c7706vvea0w6ga08
parent_id: is-01m1sp7k7txpwp2y4pbhen30jv
hold: null
hold_until: null
created_at: 2026-09-05T21:06:33.332Z
updated_at: 2026-09-06T05:27:55.029Z
started_at: 2026-09-06T03:21:56.546Z
---
BC-230: state the direction-dependent B_k containment lemma, full angle-cell coverage and D4 semantics, exact certificate fields, and refusal conditions.

## Notes

T+2 author theorem/contract frozen and source-distinct review complete. Author hashes: adaptive-core contract 7530f32b568c7b0b3b8b7fc28a56b3f2fe1c34c65ee0646b5ae2fd6a1579cee9; control matrix 262029bf695937bf0af98e0b92cb7d94e714578861a0c128205164d6cfdc49b7. Review artifact bc-230-source-distinct-review.md hash 6a7d9f8629864615d096aec4495c3f65637f201214911e5c4553250e92c23218, CONDITIONAL PASS: theorem and serialized contract sound; before BC231, strengthen P5 to direct-union and >=max boundary oracle, recast F4/F5 so named folded-cover/endpoint branches are reached rather than intercepted by derivation mismatch, make T10 a D4-balanced premise-preserving lightening mutation with updated totals/minimum, and pin P2's literal first-worst direction. Post-freeze remediation tracked in landing; no verifier/candidate exists yet.
