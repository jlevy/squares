---
title: H-285 — noncircular coarse slider floor
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-285
  kind: hypothesis
  claim: A freshly checked accepted-root guard and independent coarse-domain rational SAT envelopes give
    a conditional physical9/11 lower-slider floor with strict headroom above -1/2500.
  lane: proof
  derived_from:
  - X-048
  criterion:
    shape: determination
    metric: exact_independent_coarse_slider_floor_and_fresh_replay
    direction: criterion_met
    threshold: Both generated and fresh replay receipts require verification_passed=true AND floor_certified=true
      AND root_guard_passed=true. Full accepted root inclusion R gives -1/3<=tau0=c(s-1)<=-1/8; exact
      x9*-x11*=tau0*u+v, unit/half-angle/projection/rearrangement identities; fixed independent closed
      coarse domain; exactly8 SAT options against x9-x11,6 strict universal-support exclusions and2 +v
      survivors; positive cosine; exact floor -14333333/41666665000 and strict headroom2333333/41666665000
      above -1/2500. No H278/BWprime premise or actual leaf/global admission.
  instrument: packing/devtools/check_n17_coarse_slider_floor.py and packing/tests/test_check_n17_coarse_slider_floor.py;
    final noncircular slider contract in docs/project/research/research-2026-10-07-n17-proof-interfaces-and-lp-contract.md.
  instrument_ready: true
  regime: Full accepted root inclusion R. Independent closed |e9x|,|e9y|<=1/100,|eta11|<=1/100,|v dot
    e9|<=1/5000,b in[-1/2,1/12],q9/q11 in[-1/200,1/5000]. Physical9/11 interior non-overlap required.
    All8 SAT normals directed against Delta=x9-x11, opposite usual ordered9->11. Universal support>=1,
    no nominal corner witness.
  instance:
    axis: n
    point: 17
  priority: 1
  cost_estimate: Combined180s generation+fresh replay; enclosing owned supervisor TERM180/KILL190.26 synthetic
    controls4.64s, not target forecast.
  prereqs:
  - H-255
  replication: false
  registered: '2026-10-07'
  notes: Registered before target and accepted exp270 after generation/fresh replay1.08s at clean549c79
    source. Root loader reused only for fresh accepted-root admission. Failed guard inconclusive, malformed/premise
    mismatch refused, interruption incomplete. No H278/BWprime circular premise, LP-relaxation consequence,
    leaf or global admission. Later adapter must independently check all direct coarse premises before
    intersecting raw b. Astra hand derivation; not independently mathematically reviewed or machine-checked
---
# H-285: Coarse Slider Floor

This geometric implication starts with physical square9/11 non-overlap in an
independently declared coarse domain.
It uses neither H-278 nor the widened slider lower bound being proved.
Exact root inclusion and universal projection/support inequalities rule out six SAT
directions; the two surviving positive-v directions force the strict improved b floor.
Actual leaves must separately supply the thin v9 projection and one-sided q9/q11 bounds.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
