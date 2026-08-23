---
type: is
id: is-01m0r51fbqgm0y4tb2d09fcb82
title: Benchmark proposer-conditioned null measures for basin frequency
kind: task
status: open
priority: 1
version: 2
spec_path: explorations/packing/docs/project/reviews/review-2026-08-23-square-packing-program-and-pr14.md
labels:
  - packing
  - pr-14
  - ambiguity
  - statistical-contract
dependencies: []
parent_id: is-01m0qxpd3pnhvjh5s55b2w5gq8
created_at: 2026-08-23T20:29:52.886Z
updated_at: 2026-08-23T20:57:20.149Z
---
PR #14 ambiguity 4. Basin frequency is not a distribution-free property of the packing landscape: for named proposer distribution P and deterministic quench Q it is the probability of the preimage of a terminal component. Uniform centres and angles in one chosen box is a useful baseline, but it is parameterisation- and box-dependent, often infeasible, and cannot justify a global rarity claim. Acceptance: version P, Q, initial-side rule, feasibility conditioning or repair, random-number generator, and budget; compare raw uniform, feasible-conditioned or repaired, Sobol or Latin-hypercube, record-neighbour perturbation, continuation or surgery, and annealer-endpoint arms through one validator/quench at equal pair tests; report per-arm frequencies, confidence intervals, censoring, effective sample size and sensitivity to box size; use importance weights only where densities are known; and scope H-012 and every basin-volume statement to its measured P/Q regime.

## Notes

D-040 is the durable defect-log entry. The PR-description 12-start n=5 tally is not preserved as a replayable merged-head artifact, its counted object is unresolved, and even its point ratio does not meet H-012's threshold. Every future frequency claim is conditional on versioned P/Q/E and requires uncertainty under equal pair-test budgets.
