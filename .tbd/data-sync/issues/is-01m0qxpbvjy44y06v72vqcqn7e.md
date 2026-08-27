---
type: is
id: is-01m0qxpbvjy44y06v72vqcqn7e
title: Correct fixed-angle quench and exact-verifier contracts
kind: bug
status: open
priority: 0
version: 14
spec_path: explorations/packing/docs/project/reviews/review-2026-08-23-square-packing-program-and-pr14.md
labels:
  - packing
  - review
  - pr-14
  - technical-error
  - focus-correctness
dependencies:
  - type: blocks
    target: is-01m0qxpbheswp54a9p12640g1z
  - type: blocks
    target: is-01m0qxpc5jrdzfn205qfxfvg44
  - type: blocks
    target: is-01m0qxpcfka7ts5mnwp30zwrrs
  - type: blocks
    target: is-01m0qxpcrzkr5870j8q692t5c7
  - type: blocks
    target: is-01m0qxpd3pnhvjh5s55b2w5gq8
  - type: blocks
    target: is-01m0qxpdr07tjzxjbxffaadrjg
  - type: blocks
    target: is-01m0qxpeyc4qjhasyge91h4m06
  - type: blocks
    target: is-01m0r50mrppgcvsp2ewrac0x6z
  - type: blocks
    target: is-01m0r50x1ms53tfamwwmc5qw2z
parent_id: is-01m0r7q3f92dgx66d30wwrasbn
created_at: 2026-08-23T18:21:28.817Z
updated_at: 2026-08-27T05:57:56.750Z
---
Category: technical errors. Fixed angles do not define one LP objective unless a separating cell is fixed: solve_to_fixed_point reaches several sides from the same theta and different centers. Coordinatewise angle sweeps do not certify a local optimum. Golden search assumes unproved unimodality. NumberField accepts reducible polynomials and intervals that do not establish a unique algebraic root, invalidating complete equality and sign claims.

Acceptance: the quench contract includes cell or trajectory identity and never calls coordinatewise stationarity a local optimum without an active-set or directional certificate. Deadlines are checked inside probes. Multiple-start same-theta tests expose all reachable cells. Exact field construction verifies squarefree irreducibility and unique root isolation, or carries equivalent proof data; reducible and multi-root negative controls terminate safely. Production artifacts contain full poses and pass an independent float-plus-exact verifier. Reconcile with think-imot, think-86gm, think-25i6, and think-ty3d.

## Notes

2026-08-26 ownership reconciliation: the NumberField squarefree-irreducibility and unique-root-isolation clause is discharged by think-rsxe and D-053 and is no longer live scope here. Retain this bead for fixed-angle and mixed-angle quench semantics: cell or trajectory identity, multiple reachable cells at the same theta, coupled and nonsmooth directions, KKT or active-set evidence before any local-optimum claim, full pose evidence, and honest timeout/convergence state names. D-052 remains open. Do not use this bead to duplicate the separate numerical-to-formal promotion bridge.
