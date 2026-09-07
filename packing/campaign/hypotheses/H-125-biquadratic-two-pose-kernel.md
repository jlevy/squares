---
title: H-125 — the fixed biquadratic two-pose kernel excludes eleven
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-125
  kind: hypothesis
  claim: >-
    At side L=96/25, the fixed eleven-feature joint-D4 family in BC264's
    Session097 feature design admits positive-semidefinite coefficient blocks
    defining K=1+phi(P)^T R phi(Q), with K(P,P)<=b<11 on every contained
    unit-square pose and K(P,Q)<=0 on every distinct interior-disjoint pair.
  lane: proof
  derived_from: [X-017]
  criterion:
    shape: determination
    metric: complete kernel certificate below eleven or exact finite necessary-constraint obstruction for the fixed family
    direction: >-
      Accept only with exact PSD evidence and independently verified full diagonal
      and compatible-pair coverage at b<11. Refute with independently reconstructed
      rational nonnegative diagonal and compatible-pair weights, sum(alpha)=1,
      proving b>=1+sum(beta)>=11 through exact PSD of the projected matrices.
      A feasible outer LP, numerical objective, failed reconstruction, timeout or
      malformed packet is inconclusive. Neither route decides other feature families.
    threshold: 11
  instrument: >-
    Implemented packing/devtools/kernel_axis_lp.py and independently authored
    packing/devtools/check_kernel_axis_lp.py. The finite proposer uses exactly
    five tight axis grids and 23 necessary PSD test directions; its source and
    execution caps require a separate prospective experiment protocol. Both
    implementations passed source-free controls and independent max-thinking
    code review at the Session097 checkpoint. Actual immutable engine/protocol
    checks and publication remain prerequisites to invocation. No complete
    continuum verifier is implemented or priced. Source-free build admission is
    not target readiness.
  instrument_ready: true
  regime: >-
    n=11, L=96/25, exactly the declared eleven features and sixteen joint-D4
    coefficients, all contained poses modulo local quarter-turn, legal touching
    retained; only joint physical container symmetries
  instance: {axis: n, point: 11}
  priority: 2
  cost_estimate: one fixed finite LP and independent exact reader, prospectively capped separately after readiness
  prereqs: [BC264 independent kernel admission, frozen instrument, source-free controls, independent implementation review, prospective experiment protocol]
  replication: false
  registered: '2026-09-07'
  notes: >-
    Registered during source-free implementation and before scientific source
    construction or execution. Increasing degree, changing features, expanding
    the source or retrying a failed solve requires a new allocation and, when
    changing the claim, a new hypothesis. The cubic obstruction does not decide H125.
---
# H125 — One Biquadratic Kernel Family

This is the concrete first family under
[H114](H-114-two-pose-kernel-exclusion.md), not a claim about all two-pose kernels.
The [feature design](../series/series-000-smoke-and-calibration/results/agenda-027/bc-264-kernel-feature-design.md#the-sole-proposed-family)
fixes the order and coefficient blocks. With centered coordinates $u,v$, its features
are $z=(1,u^2+v^2,u^2v^2,\cos4\theta)$, the three scalar features
$\sin4\theta$, $u^2-v^2$, $uv$, and vector copies $(u,v)$ and $(uv^2,u^2v)$.
The positive-semidefinite blocks are a symmetric $4\times4$ matrix $A$, three
nonnegative scalars, and $B\otimes I_2$ for a symmetric $2\times2$ matrix $B$.

The first proposed test can only refute this family. It uses a finite set of exact
axis-aligned poses and an outer LP relaxation of the PSD conditions. Its separate
reader must reconstruct containment, compatibility, weights and projected matrices
from the fixed source. Exact normalization and PSD imply
$b\ge1+\sum\beta$; a value at least eleven is a family obstruction.
The [independent admission](../series/series-000-smoke-and-calibration/results/agenda-027/bc-264-kernel-acceptance-review.md#post-freeze-admission-the-finite-lp-instrument)
retains the block-trace factor, sparse-support semantics and required refusal controls.

The source-free instruments and their independent reviews are complete; engine
`d6f0c403` passed its immutable push gate. The prospective
[exp129](../series/series-000-smoke-and-calibration/experiments/exp-129-h125-finite-kernel-obstruction.md)
did not launch: its protocol checks failed a stale documentation-control anchor,
and the22:20 UTC launch cutoff passed. Its zero scientific time and blocked guard
do not refute this family. Instrument readiness remains true; a fresh operational
allocation, passing record checks and published admission are required before the
still-unspent first invocation. The full engine checkpoint remains separate.

No target has run. A finite LP feasible point is not a PSD kernel candidate, and
even a PSD candidate would still need full-domain sign and diagonal verification.
Neither a refutation here nor an inconclusive run changes the published packing bound.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
