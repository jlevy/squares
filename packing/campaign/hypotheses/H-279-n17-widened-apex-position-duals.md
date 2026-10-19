---
title: H-279 — an exact conditional apex radius from retained n17 position duals
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-279
  kind: hypothesis
  claim: >-
    The 58 retained signed-position duals evaluated at slider origin have
    nonnegative weights and row-l1 residual epsilon<1 on the 29-column positive
    position matrix over the accepted root inclusion interval. Their exact
    Lipschitz mass C>0 supplies alpha0=min(1/5000,(1-epsilon)/(10000*C)),
    q0=alpha0/2 and position headroom at most1/10000 for the stated conditional
    physical-packing apex bridge to the accepted local theorem.
  lane: proof
  derived_from: [X-048]
  criterion:
    shape: determination
    metric: complete_exact_position_duals_and_apex_radius_replay
    direction: criterion_met
    threshold: All58 directions,52 positive rows,29 position columns and nonnegative exact weights; epsilon<1,C>0,positive alpha0/q0, accepted feature/root/local-domain joins and fresh replay agreement.
  instrument: >-
    packing/devtools/check_n17_widened_apex.py; exact reconstruction from the
    accepted exp248 run002 affine duals and accepted H278 feature certificate.
    The finite-geometry implication is Astra's separately scoped hand proof in
    docs/project/research/research-2026-10-07-n17-proof-interfaces-and-lp-contract.md.
  instrument_ready: true
  regime: >-
    n17 fixed declared container [0,S_exact_root]^2; side increment zero.
    Position radius1/100, half-angle radius1/200, sliders in B_W'. Accepted
    exp237 root inclusion enclosure; 58 signed position duals from exp248
    run002, integer numerators/2^44, evaluated exactly at origin. All angle and
    side columns removed; wall Lipschitz1/2,pair Lipschitz12/5. No LP solve.
  instance: {axis: n, point: 17}
  priority: 1
  cost_estimate: At most180 seconds combined production and fresh receipt replay.
  prereqs: [H-255, H-257, H-258, H-268, H-278]
  replication: false
  registered: '2026-10-07'
  notes: >-
    Exact finite residual/radius checks and sole Astra hand implication have
    separate assurance. Root feature tightness, C2 slide invariance, C10 walls
    and the accepted local theorem remain explicit premises. No automatic
    stronger LP-union rigidity, annulus coverage, outer capture, or enlarged
    slider coverage follows. Failed/missing directions, weights, domain or
    premise bindings, epsilon>=1,C<=0,nonpositive radii or replay disagreement
    refuse acceptance. Freeze source and criterion before target evaluation.
---
# H-279: Exact Conditional Apex Bridge

The retained local duals already contain the necessary signed-position witnesses.
This round evaluates them at the slider origin and bounds their residuals over the
accepted exact-root enclosure without a new solve.
Astra’s argument explains why the position projection applies throughout B_W'.

A successful finite check supplies an inner half-angle cube for the conditional
physical-packing argument.
It does not cover the annulus or deliver arbitrary packings into the widened region.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
