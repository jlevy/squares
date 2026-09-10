---
title: "H-158 \u2014 the necessary parent domain excludes the saved residual or an owner class"
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-158
  kind: hypothesis
  claim: For exp151's direction-6 saved residual on selected tuple (0,0,0,7), either the residual centre
    lies outside its own necessary unit-parent box, or at least one selected owner class has a positive
    B-only separation witness but no positive separation after the complete global-D parent restriction.
  lane: proof
  derived_from: [X-026]
  criterion:
    shape: determination
    metric: Exact residual self-exclusion or matched B-only-positive and parent-restricted-nonpositive
      separation for one complete selected owner class
    direction: positive
    threshold: '0'
  instrument: packing/devtools/wall_owner_parent_experiment.py
  instrument_ready: true
  regime: exp151 direction-6 residual; tuple (0,0,0,7); q=96/25; B=9977/10000;
    D=207107/90000000; original marks and physical corner maps; complete 361-direction residual authority;
    181 frames per selected owner; evaluation order TR, BL, BR, TL.
  instance:
    axis: n
    point: 11
  priority: 1
  cost_estimate: One 90-second scientific allowance after input loading, inside one 120-second externally
    supervised process with two-second termination grace.
  prereqs:
  - Target-free parent runner and complete import closure admitted by independent Astra Max review after
    56 focused tests, deadline and readback adversaries, Ruff and BasedPyright.
  - Clean committed prospective exp156 with a fresh result path and the exact execution revision resolved
    from full HEAD.
  replication: false
  registered: '2026-09-10'
  notes: >-
    Exp156 completed at source-bound revision 5f6c50c4866921f366073511ac28713b0d1267d2 with outcome
    b-only-incompatible. The residual survived its necessary parent box, but the first selected owner was
    already incompatible under the old B-only model after all 181 frames and literal replay. Since the
    parent-restricted feasible set is a subset of the B-only set, parent-domain gain is impossible for that
    TR class. The redundant TR parent arm and later owners were not run, so H-158 remains unresolved: neither
    accepted nor rejected. Exp156 permits no rerun or later-owner continuation. A separately registered
    experiment may skip TR and test BL, BR and TL under a new stopping rule. Positive parent-restricted
    witnesses for all three, combined with TR's B-only incompatibility, would reject H-158 for individual
    elimination of this fixed pose. Exp150 witnesses may not replace a matched B-only control.
---
# H158: Necessary Parent Geometry at the Saved Residual

Exp151 retained one exact direction-6 residual after the first six directions became
covered. H-158 asks whether necessary unit-parent geometry excludes that fixed pose
directly or removes one owner class that the B-core model alone permits.

The frozen rule uses, for each retained unit direction `r`, `S=|r.x|+|r.y|`,
`T=||r.x|-|r.y||`, and `e=max(B*S/2,1/2,(S-T*D)/(2+D^2))`. It intersects each original
anchored owner domain with `[e,q-e]^2`. The residual receives its own necessary
parent-box check and no owner mark constraint.

The [analytic contract](../../cases/n11_five_dot_cover/unit-parent-centre-contract.md)
proves the restriction.
The
[independent runner review](../../../docs/project/reviews/review-2026-09-10-n11-parent-runner-independent.md)
admits the target-free implementation, complete source binding, exact replay, clocks,
and result reader.
Exp156 then ran once at `5f6c50c4866921f366073511ac28713b0d1267d2` and
completed with `b-only-incompatible`.

The one registered experiment must report these outcomes separately:

- `residual-self-excluded`: accept because the fixed residual centre fails its own
  necessary parent box.
- `owner-domain-gain`: accept because the same selected owner has a newly computed,
  independently replayed positive B-only witness and an exhaustive nonpositive
  parent-restricted result over all 181 frames.
  An exactly all-empty restricted class also qualifies, with a null maximum.
- `b-only-incompatible`: record an old-model exclusion after exhausting all 181 B-only
  frames for that owner.
  The parent-restricted set is a subset of the B-only set, so parent-domain gain is
  impossible for that owner.
  The result does not resolve possible gain at later untested owners.
- `no-owner-domain-exclusion`: reject H-158 after the residual survives and all four
  owners have positive parent-restricted witnesses.
- `incomplete` or `invalid`: preserve the completed prefix without a universal
  conclusion.

This is one fixed-pose, individual-owner comparison.
It does not establish a compatible unit-parent angle, simultaneous four-owner
feasibility, a neighbourhood exclusion, an owner-routing theorem, or a global n11 bound.
The residual survived its parent box, but the old B-only model already excludes
`TR / bottom-left:m1:j7` after all 181 frames.
Because every parent-restricted TR placement is also a B-only TR placement, this exact
negative maximum rules out parent-domain gain at TR without running the redundant
restricted arm. The registered protocol then stopped without testing any later owner.
H-158 therefore remains unresolved.
A future protocol may skip TR and test `BL`, `BR` and `TL`, but it must be prospectively
registered as a new experiment.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
