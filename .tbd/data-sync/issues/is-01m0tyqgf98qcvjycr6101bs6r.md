---
type: is
id: is-01m0tyqgf98qcvjycr6101bs6r
title: Replace polished with unambiguous evidence terminology
kind: bug
status: closed
priority: 1
version: 6
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-frontier-assurance-and-verification.md
labels:
  - packing
  - terminology
dependencies: []
parent_id: is-01m0typjn7s866m042zsemybj6
created_at: 2026-08-24T22:37:18.184Z
updated_at: 2026-08-25T07:24:21.135Z
closed_at: 2026-08-25T07:24:21.123Z
close_reason: The definitive docs and v2 contracts now reserve verified for formal evidence, use numerically checked for numerical work, retire polished and ambiguous arbitrary-precision labels, and define campaign/session/series/experiment/round/run consistently.
resolution: null
duplicate_of: null
---
The evidence label polished is optimization jargon, not a mathematical assurance level, and currently covers both solver-scale refinement and a 160-digit multiprecision numerical check. Define and migrate to numerical-f64, numerical-multiprecision with actual precision and tolerance, interval-certified, exact-algebraic, proof-audited, and proof-assistant-checked as applicable. Keep search-stage operations separate from evidence status.
