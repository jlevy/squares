---
title: "H-150 \u2014 one site can hit both saved escaping cores"
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-150
  kind: hypothesis
  claim: The closed escaping B-cores retained by exp149 and exp151 have a nonempty intersection, so one
    replacement sixth site can hit both.
  lane: proof
  derived_from: []
  criterion:
    shape: determination
    metric: The two closed escaping cores have at least one common point
    direction: positive
    threshold: '1'
  instrument: packing/devtools/wall_owner_sixth_site_screen.py
  instrument_ready: true
  regime: Same tuple (0,0,0,7), q=96/25 and B=9977/10000; exact source-bound exp149 axis core and exp151
    owner-006 core.
  instance:
    axis: n
    point: 11
  priority: 1
  cost_estimate: One 60-second external process plus two-second grace and 30-second internal guard; no
    retry.
  prereqs:
  - Both escaping cores replay against their declared original-five/six-site and four-patch domains.
  - Admitted source and point/segment-aware controls; clean published prospective protocol.
  replication: false
  registered: '2026-09-09'
  notes: Accept only nonempty closed intersection, retaining dimension, exact vertices and their canonical
    arithmetic mean. This is a necessary two-witness feasibility screen, not a full cover. Empty intersection,
    independently checked by strict square SAT, rejects every D-plus-one-site cover of this relaxed tuple
    domain. No arbitrary six-site or global packing claim follows.
---
# H150: Is Any Sixth Site Still Possible?

Both saved cores avoid the original five sites D. Any additional site completing that
fixed cover must lie inside both closed cores.
An empty intersection rules out the whole D-plus-one-site family; a nonempty
intersection supplies only one necessary candidate.
Points and segments count as nonempty.

The
[reviewed decision contract](../../cases/n11_five_dot_cover/after-six-dot-refutation-strategy.md)
fixes the exact screen.
[Source admission](../../cases/n11_five_dot_cover/sixth-site-screen-source-admission.md)
is GO: 10 screen controls pass, and the independent combined suite passed 23 tests in
0.99 seconds. Exp152 now accepts this necessary screen: the exact intersection is a
two-dimensional quadrilateral with a verified common site.
No full cover follows.
The
[convex feasibility analysis](../../cases/n11_five_dot_cover/sixth-site-cutting-contract.md)
explains a conditional bounded continuation and why three cores can certify
infeasibility without guaranteeing three search iterations.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
