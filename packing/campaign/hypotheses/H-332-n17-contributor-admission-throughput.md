---
title: H-332 — the four fully reported contributor certificates replay and admit within bounded resources
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-332
  kind: hypothesis
  claim: >-
    Each of the four contributor certificates with reported unmodified standing-FULL
    receipts (#358 classes C1 and C2, #413 rows 1 and 2), fetched from their immutable
    packages, passes a same-object FULL replay with the PR 452 standing BB verifier
    within 4 hours and 8 GB of sampled RSS, passes the source-cell enclosure guard, and
    joins to the ordinary ledger by its exact named-cell D4 class, removing at least the
    21 orbits of the #358 union from the residue.
  lane: proof
  derived_from: [X-051]
  criterion:
    shape: determination
    metric: >-
      Per certificate: acquisition digest match, header guard verdict, FULL replay
      verdict with wall time and peak sampled RSS, and the census consumer's marginal
      orbit count after admission.
    direction: >-
      Confirm when all four pass within the ceilings and the consumer reports at least 21
      fewer orbits. A replay above either ceiling, a guard refusal or a failed join
      refutes it for that certificate; the others are still counted.
    threshold: 4 of 4; 4 hours and 8 GB each; at least 21 orbits removed.
  instrument: >-
    devtools.verify_n17_bb_certificate at main after PR 452 (digest 10db91c2...), the
    exp-310 header preflight, the exp-311 acquisition path with its RSS monitor repaired
    so that a slow ps sample does not stop the run, and devtools.census_n17_certified
    for the join.
  instrument_ready: true
  regime: >-
    n = 17; the H-266 cover at U; the contributor packages at the revisions their
    manifests pin; one FULL replay per certificate on a host with 16 GB; the 480 GB row
    33 explicitly excluded.
  instance: {axis: n, point: 17}
  priority: 2
  cost_estimate: >-
    Up to 16 CPU-hours of replay (the contributor reports 5,906 s and 2,220 s for the
    #358 classes on their host) plus about 10 agent-hours for custody, joins and the
    admission review.
  prereqs: [H-318, H-319]
  replication: false
  registered: '2026-10-09'
  notes: >-
    X-051's route H. The C2 replay of 8 October stopped incomplete after 480 s because
    the RSS monitor's one-second query timed out, not because of memory; that monitor is
    the first thing to repair. The #413 roster projects conditionally onto 2,234 orbits,
    but only rows 1 and 2 have unmodified FULL receipts, rows 3 and 4 used parallel node
    checks, and the remaining 29 rows are fast-verifier or computed only; admitting the
    four is the honest first slice and prices the rest.
---
# H-332: Admitting What Contributors Have Verified

**Mechanism.** A certificate the standing verifier passes in full, bound to immutable
objects and joined to the cover by its exact cells and $D_4$ class, is an admission like
any other; the lifetime repair of PR 452 removes the retained-node growth that kept the
largest certificates from fitting.
Four certificates have reported FULL receipts; replaying them here is the step from
report to admission.

**Falsifier.** A replay above 4 hours or 8 GB, a header-guard refusal, or a failed
original-domain join on any of the four.

**Expected information.** The first census movement from contributor work, and a
measured admission cost per orbit that decides whether the remaining 29 rows are worth
full replay and in what order.

**Limits.** Repackaged manifests need fresh object and receipt joins; a FULL pass is not
a review, and the think-t41a enclosure prerequisite applies to every externally produced
branch-and-bound certificate.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
