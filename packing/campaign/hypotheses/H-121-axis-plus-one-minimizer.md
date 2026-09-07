---
title: H-121 — some global minimizer has an axis-plus-one-angle representative
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-121
  kind: hypothesis
  claim: >-
    Some global minimizing packing of eleven unit squares has every actual
    orientation in {0, theta} modulo pi/2 for one theta; the axis class may be empty.
  lane: proof
  derived_from: [X-018]
  criterion:
    shape: determination
    metric: existence of a global axis-plus-one-angle minimizing representative
    direction: >-
      Accept only with an independently checked global representative theorem,
      covering every relevant minimizer alternative and contact degeneration.
      Reject only by ruling out every such minimizing representative, for example
      by a verified packing strictly below a proved lower bound for this entire
      restricted family. A high-angle feasible or local-minimum witness alone,
      numerical recurrence, a partial release theorem and timeout are insufficient.
    threshold: one nonaxis actual orientation
  instrument: >-
    Proposed complete finite angle-elimination argument or sufficient global
    orientation-rank reduction, independently reviewed against all contact changes,
    minimizing premises and alternative representatives.
  instrument_ready: false
  regime: >-
    Global side minimization for n11 with legal touching, all centers and actual
    orientations free, and container orientation fixed; existential representative
  instance: {axis: n, point: 11}
  priority: 2
  cost_estimate: one bounded lemma or obstruction; cost of a global proof is unknown
  prereqs: [complete representative reduction with all alternatives, independent global proof review]
  replication: false
  registered: '2026-09-07'
  notes: >-
    H-TBD-NORMAL-FORM made precise under the broad H117 question. H112 and H113
    concern lower bounds on restricted families, not existence of representatives.
    BC274 owns this narrower proof obligation without taking over BC267's KKT audit.
---
# H-121 — An Axis-Plus-One-Angle Minimizer

[X-018](../explorations/X-018-hybrid-strength-and-angular-release.md) gives the
motivation and missing global implication.
A segment-equality graph of rank at least ten is sufficient, but not necessary:
disconnected components can share an angle.
Point contacts and small stress support do not force orientation equality.

Choose a global minimizer with the fewest nonaxis angles.
A proposed elimination proof must supply a finite feasible motion at nonincreasing side
through releases, new contacts and degeneracies; an infinitesimal flex does not suffice.
H-120 tests one restricted exclusion and cannot accept this global claim.

Even an accepted normal form combined with H-112 leaves the other multiplicities open.
A complete axis-plus-one-family lower bound, or the stronger H-113 theorem, would supply
the remaining value argument.
Equality classification would still be needed for uniqueness.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
