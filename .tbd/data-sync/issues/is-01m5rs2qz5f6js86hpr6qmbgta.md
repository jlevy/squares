---
type: is
id: is-01m5rs2qz5f6js86hpr6qmbgta
title: "Import Jatloe et al.: Lean proof s(12) = 4, Jatloe12SquaresFormalized d0caf45 (#810)"
kind: task
status: in_progress
priority: 1
version: 3
delegate: coord-n12-1025
labels:
  - result-import
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-25T05:38:35.108Z
updated_at: 2026-10-25T06:04:47.674Z
started_at: 2026-10-25T05:38:38.919Z
---
Owner report 2026-10-25 (X post https://x.com/ManassehA06/status/2113097037306569124 and its reply naming the repo); tracking issue https://github.com/jlevy/squares/issues/810. Source: Queuingtheorydotcom/Jatloe12SquaresFormalized at d0caf4532a7ead68be1389ef87387b126fc2e0ab (tag n12-verified-2026-10-16), Lean/Proofs/N12-jatloe, theorem N12Compact.Final.optimality : S12.packingConstant12 = 4. Triage 2026-10-25: closure 5377 modules, 0 missing, 0 sorry, 0 axiom decls, 2572 native_decide; source audit 3 standard + 1624 native axioms; accepting run reused cached objects. Upstream EvolvingPrograms/SquaresLean@1f60d41 not publicly reachable. Stages: packet, register as reported (S4/S5 candidate), statement audit, math review, replay priced (above cap).

## Notes

Statement audit (w-n12-audit-1025, 2026-10-25): docs/project/reviews/review-2026-10-25-n12-lean-formalization-statement-audit.md, commit 40e15dbb8 on branch worktree-agent-aa8ad7d72a4de3571 (not pushed; not yet mapped in docs/project/document-map.yaml).
Verdict: statement faithful (unrestricted rotations, open squares, closed container, contact allowed; sInf = 4 forces nonempty + bdd below, grid attains 4); final theorem premise-free; trust base = kernel + 3 standard + 1,624 native_decide axioms = exactly the calls of 1,525 S12 declarations (948 further calls in 749 decls compiled but off the path).
Findings: none blocking. M-1 compiler trust (wording); M-2 accepting run compiled 0 modules, upstream private, no inspectable build; m-1 statement defs import S12.To117 (109-module statement closure, 723 native calls); m-2 Mathlib pinned only in verification/toolchain-lock.json (Lake manifest uses path packages); N-1 stale comments; N-2 off-path native calls; N-3 autoImplicit default.
Records lane: encode as source's report (like E-n011-lean-formalization-report); counts beyond devtools.lean_closure came from unretained scratch programs (OR-1: make a tool before citing).
