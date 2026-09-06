---
type: is
id: is-01m1sp9z7ntvtwrpp9a9t9k4r8
title: Formalize the adaptive witness-core theorem
kind: task
status: closed
priority: 1
version: 8
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
updated_at: 2026-09-06T06:03:23.180Z
started_at: 2026-09-06T03:21:56.546Z
closed_at: 2026-09-06T06:03:23.179Z
close_reason: Completed the adaptive-core theorem and executable control-contract scope. The source-distinct theorem review, four post-freeze repairs, fresh xhigh implementation review, and max coordinator disposition all pass; verifier implementation remains BC-231 behind BC-220.
resolution: null
duplicate_of: null
---
BC-230: state the direction-dependent B_k containment lemma, full angle-cell coverage and D4 semantics, exact certificate fields, and refusal conditions.

## Notes

BC-230 complete at theorem-and-control-contract scope. Frozen theorem hash 7530f32b568c7b0b3b8b7fc28a56b3f2fe1c34c65ee0646b5ae2fd6a1579cee9; frozen T+2 matrix hash 262029bf695937bf0af98e0b92cb7d94e714578861a0c128205164d6cfdc49b7; original source-distinct review hash 6a7d9f8629864615d096aec4495c3f65637f201214911e5c4553250e92c23218. Post-freeze reconciled matrix hash 4911b76161f62c8ece32b3fd7eb8866f2f2bd18dbf2d003ea94f29aaab30535d, self-normalized digest 7b856c12bdf6b0eced0ba0bb89382f2049fb67ea6b5850b7814680b369a6533d. Fresh xhigh implementation review passed P5, F4/F5, T10 and P2; max coordinator accepted the contract. No adaptive verifier or candidate exists. BC-231 remains behind BC-220.
