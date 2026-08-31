---
type: is
id: is-01m136knhk454ntqdx6a00gccq
title: "Registry: record that n=28 and n=39 provably have no radical closed form"
kind: task
status: closed
priority: 2
version: 2
labels:
  - packing
dependencies: []
parent_id: is-01m136khr29m0p8t6q8kybd562
created_at: 2026-08-28T03:28:56.369Z
updated_at: 2026-08-28T03:46:18.210Z
closed_at: 2026-08-28T03:46:18.208Z
close_reason: "Landed in PR #51 (squashed to main)."
resolution: null
duplicate_of: null
---
Verified with sympy galois_group: n=28 minimal polynomial s^6-24s^5+212s^4-812s^3+1025s^2+882s-1615 is irreducible with Galois group S6 (not solvable); n=39 9s^5-171s^4+999s^3-1959s^2+1636s+166 is irreducible with S5 (not solvable). Both roots match their recorded values. Their exact_form: null is therefore correct and PERMANENT, not a transcription gap, and the registry should say so to stop future searches. n=70 23s^4-742s^3+8848s^2-45876s+86229 is degree 4 with S4, so solvable in radicals, but the expression is impractically large.
