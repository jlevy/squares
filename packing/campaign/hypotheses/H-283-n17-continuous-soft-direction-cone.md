---
title: H-283 — one exact continuous n17 soft-direction cone with six free angles
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-283
  kind: hypothesis
  claim: >-
    Exact nonnegative finite-gap weights certify a strict homogeneous contradiction
    on the punctured negative square-16 cone times six free angle coordinates,
    over the complete accepted root inclusion interval, widened slider box and
    position tube, covering every selected owner branch and retaining the endpoint.
  lane: proof
  derived_from: [X-048]
  criterion:
    shape: determination
    metric: exact_continuous_cone_and_fresh_receipt_replay
    direction: criterion_met
    threshold: >-
      cone_certified=true; all 32 centre coefficients cancel, exact side and
      constant identities, F2=Pi2/[t(1+t)(1+t^2)(1+beta^2)] with Pi2=0 joined
      to fresh root verification; strict positive c,s,d_r,e_r and normalization
      denominator, all 16 weights nonnegative, K<=-1/50, M<=50, exact positive
      gamma=638375/40961024, complete H278/domain/256-owner joins and fresh replay.
  instrument: >-
    packing/devtools/check_n17_widened_cone.py, with target-free symbolic,
    outward rational interval, custody, CLI roundtrip and tamper controls in
    packing/tests/test_check_n17_widened_cone.py; Astra's continuous-cone contract
    in docs/project/research/research-2026-10-07-n17-proof-interfaces-and-lp-contract.md.
  instrument_ready: true
  regime: >-
    Fixed exact-root container [0,S*]^2, complete accepted inclusion root R,
    B_W'=[0,1/4]x[-1/2500,1/12]x[-1/8,1/16], position radius 1/100.
    q16=-r with 0<r<=1/200; nine labels{1,2,3,9,10,13,14,15,17}
    satisfy |qj|<=r/2048; six unused labels{4,5,7,8,11,12} range freely
    in [-1/200,1/200]. Intervals checked on closed r=[0,1/200], but
    r=0 is not excluded. Six wall and ten pair weights; eight non-16
    weighted pairs use 24/5 perturbation allowance, two owner-16 pairs use 1.
    Reconstruct all 27 retained options/19 pairs/256 branches, both owner
    variants and the weighted-label incidence. No LP solve, seed or tuning.
  instance: {axis: n, point: 17}
  priority: 1
  cost_estimate: At most 180 seconds combined generation and fresh CLI replay.
  prereqs: [H-255, H-278]
  replication: false
  registered: '2026-10-07'
  notes: >-
    One continuous conditional cone, not a complete angular cover, global residue
    exclusion, capture theorem or side bound. The r=0 endpoint remains retained;
    H279 is a separate coverage/apex join and is not logically needed here.
    Fresh reconstruction must agree. Honest failed sign or mass bounds leave
    the cone inconclusive; malformed or mismatched premises refuse. Interrupted
    generation/replay is incomplete. No failure is evidence of a feasible packing.
    The uniform finite-geometry perturbation implication is Astra's hand proof,
    without independent mathematical review or end-to-end formal verification.
---
# H-283: One Continuous Soft-Direction Cone

The sixteen weighted finite gaps telescope at the same radial turn: all center
coefficients cancel, and their sum is $d_rA+e_rB-1$. The exact root identity removes the
constant residual, giving $2r(K-r)/(1+r^2)$. A small interval residual cannot replace
that zero because it would dominate the negative linear allowance as $r$ approaches
zero.

The checker reconstructs both owners of every weighted binary pair, proves the wall and
pair weight-mass identities, and derives the constrained-label roster.
Only the nine non-16 labels in weighted rows must scale with $r$; the six other labels
retain their full angle ranges.
The accepted H-278 forcing premise joins physical packings in the declared region to all
256 selected choices.

Acceptance requires the finite sign/mass checks and a fresh exact replay, with
$\gamma=638375/40961024>0$. The strict contradiction applies only when $r>0$. The
endpoint, remaining directions and global capture obligations remain open.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
