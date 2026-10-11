---
title: "H-297 \u2014 fixed-angle feasible-center relaxation"
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-297
  kind: hypothesis
  claim: The fixed-angle wall-and-owned-point center domain admits a deterministic exact pooled relaxation
    witness.
  lane: proof
  derived_from:
  - X-048
  criterion:
    shape: determination
    metric: fixed_angle_owned_point_relaxation_witness
    direction: criterion_met
    threshold: After accepted complete exp286 union miss and exp287 containment-only miss with fresh
      verification, reconstruct every row26 residual piece in retained order. Clip exact fixed-angle
      numeric walls and all conditional owner0 signed strips first. Continue empty/closed-covered
      pieces; the first uncovered piece supplies one deterministic first-gap candidate. Fresh pose
      tests must all pass for owned_point_relaxation_witness. Candidate pose failure refuses, with
      no alternate. All pieces empty/covered is only criterion-missed, not exclusion, because closed
      obstacles and the strict fixed margin are conservative. No17packing, capture, census, unconditional/global
      claim.
  instrument: packing/devtools/probe_n17_pooled_feasible_center.py
  instrument_ready: true
  regime: Fixed tau53/128, same accepted original-parent pools/H290/exp280/H292-282 and guardI, no284geometry.
    ALL286row26pieces in retainedorder; T=P clipped FIRST to exacttau numeric walls with h=(c+s)/2
    and conditional Q0 signed body strips using mu=2^-20. Foreign F_j=Q_j-EXACT closed zero-centered
    unit square at tau, not the innercore. Exact CLOSED union coverage precedes deterministic first
    sweepx/firstgap midpoint or degenerate parameter branch. Covered/empty pieces continue; firstcandidate
    pose failure REFUSES, no alternate. Fresh complete T/F/coverage/selection/pose reconstruction;
    six frozen small accepted input files only, no originalbulk/parent/union replay.
  instance:
    axis: n
    point: 17
  priority: 1
  cost_estimate: One worker60s construction+60s fresh inside120s combined, TERM120/KILL130; sampled4096MiB
    PER live process with ownedgroup wall/cleanup. Each acceptedinput10MiB/output64MiB; normalizedgeometry4096bits;
    pool128,T256,exactF132,<=256row26pieces,totalforeign Minkowski vertex pairs8192; existing2048edges/2100000prospective
    comparisons before trusted exactsweep, deadlinebefore/after plus supervisor. No unreduced homogeneous
    integer-product cap or allocation-time/instantaneous-peak claim.
  prereqs:
  - H-295
  - H-296
  replication: false
  notes: Author22 target-free controls passed1.37s; independent22 passed0.99s; Ruff/BasedPyright zero;
    sole-Astra mathematical source review clear. Actual288 geometry unrun before registration.
  registered: '2026-10-07'
---
# Fixed-Angle Feasible-Center Relaxation

Fixed tau53/128, same accepted original-parent pools/H290/exp280/H292-282 and guardI,
no284geometry. ALL286row26pieces in retainedorder; T=P clipped FIRST to exacttau numeric
walls with h=(c+s)/2 and conditional Q0 signed body strips using mu=2^-20. Foreign
F_j=Q_j-EXACT closed zero-centered unit square at tau, not the innercore.
Exact CLOSED union coverage precedes deterministic first sweepx/firstgap midpoint or
degenerate parameter branch.
Covered/empty pieces continue; firstcandidate pose failure REFUSES, no alternate.
Fresh complete T/F/coverage/selection/pose reconstruction; six frozen small accepted
input files only, no originalbulk/parent/union replay.

After accepted complete exp286 union miss and exp287 containment-only miss with fresh
verification, reconstruct every row26 residual piece in retained order.
Clip exact fixed-angle numeric walls and all conditional owner0 signed strips first.
Continue empty/closed-covered pieces; the first uncovered piece supplies one
deterministic first-gap candidate.
Fresh pose tests must all pass for owned_point_relaxation_witness. Candidate pose
failure refuses, with no alternate.
All pieces empty/covered is only criterion-missed, not exclusion, because closed
obstacles and the strict fixed margin are conservative.
No17packing, capture, census, unconditional/global claim.

One worker60s construction+60s fresh inside120s combined, TERM120/KILL130;
sampled4096MiB PER live process with ownedgroup wall/cleanup.
Each acceptedinput10MiB/output64MiB; normalizedgeometry4096bits;
pool128,T256,exactF132,<=256row26pieces,totalforeign Minkowski vertex pairs8192;
existing2048edges/2100000prospective comparisons before trusted exactsweep,
deadlinebefore/after plus supervisor.
No unreduced homogeneous integer-product cap or allocation-time/instantaneous-peak
claim.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
