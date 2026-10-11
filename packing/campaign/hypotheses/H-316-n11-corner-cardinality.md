---
title: H-316 — Correlated Four-Corner n11 Cardinality
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-316
  kind: hypothesis
  claim: Correlated Four-Corner n11 Cardinality
  lane: proof
  derived_from:
  - X-048
  criterion:
    shape: determination
    metric: n17-n11-corner-cardinality
    direction: criterion_met
    threshold: Complete exact 216 cell/class feasibility tests on original convex cells with physical
      wall constraints, shared x/y/h and exact 2*h*h<=1 vertex test; all95 named distance-two assignments
      then receive complete four-count DP with each count<=10. Endpoint assignment must survive calibration.
      Primary at least one fresh-verified ordinary n11 corner-cardinality obstruction with complete95
      accounting; all95 survivors retire this exact four-corner relaxation. Negative certificates retain
      all18 reachable-frontier bitmaps; positives retain17 independently checked pattern witnesses. All
      input/domain/theorem joins and full fresh payload must match. No global optimality, capture or automatic
      census admission; refusal/resource stop unresolved. No denser window search on unchanged miss.
  instrument: packing/devtools/check_n17_n11_corner_cardinality.py
  instrument_ready: true
  regime: Complete exact 216 cell/class feasibility tests on original convex cells with physical wall
    constraints, shared x/y/h and exact 2*h*h<=1 vertex test; all95 named distance-two assignments then
    receive complete four-count DP with each count<=10. Endpoint assignment must survive calibration.
    Primary at least one fresh-verified ordinary n11 corner-cardinality obstruction with complete95 accounting;
    all95 survivors retire this exact four-corner relaxation. Negative certificates retain all18 reachable-frontier
    bitmaps; positives retain17 independently checked pattern witnesses. All input/domain/theorem joins
    and full fresh payload must match. No global optimality, capture or automatic census admission; refusal/resource
    stop unresolved. No denser window search on unchanged miss.
  instance:
    axis: n
    point: 17
  priority: 1
  cost_estimate: 120s construction+120s separate fresh; outerTERM240/KILL250, one worker,sampled4GiB currentRSS
    perliveprocess;10MiBdescriptor/64MiBoutput/4096bitgeometry;4Mvertex triples/64Mrow tests/64M DP transitions/3Mperstate/14641states
    per layer.
  prereqs:
  - H-312
  replication: false
  notes: Prospective before actual target classifications. SoleAstra mathematical SOURCE CLEAR; author26
    target-free controls PASS19.70s, independent ROOT FULL26 PASS3.32s; Ruff/format/BasedPyright zero.
    Closed membership aliases deliberately undercount guaranteed memberships at seams, giving a sound
    relaxation. Existing T061 n11 theorem and named partition/D4 scope are inherited explicitly. No actual
    classifications or DP predicates evaluated before registration.
  registered: '2026-10-07'
---
# Correlated Four-Corner n11 Cardinality

Complete exact 216 cell/class feasibility tests on original convex cells with physical
wall constraints, shared x/y/h and exact 2*h*h<=1 vertex test; all95 named distance-two
assignments then receive complete four-count DP with each count<=10. Endpoint assignment
must survive calibration.
Primary at least one fresh-verified ordinary n11 corner-cardinality obstruction with
complete95 accounting; all95 survivors retire this exact four-corner relaxation.
Negative certificates retain all18 reachable-frontier bitmaps; positives retain17
independently checked pattern witnesses.
All input/domain/theorem joins and full fresh payload must match.
No global optimality, capture or automatic census admission; refusal/resource stop
unresolved. No denser window search on unchanged miss.

Prospective before actual target classifications.
SoleAstra mathematical SOURCE CLEAR; author26 target-free controls PASS19.70s,
independent ROOT FULL26 PASS3.32s; Ruff/format/BasedPyright zero.
Closed membership aliases deliberately undercount guaranteed memberships at seams,
giving a sound relaxation.
Existing T061 n11 theorem and named partition/D4 scope are inherited explicitly.
No actual classifications or DP predicates evaluated before registration.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
