---
title: H-251 — a rectangle-density certificate in tokoharu's format proves s(82) >= 93/10, and so s(n) >= 93/10 for n = 82..85
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-251
  kind: hypothesis
  claim: >-
    A D4-symmetrized rectangle-density certificate in tokoharu's format, with exact
    total mass strictly below 82 at side 93/10 and shrink B = 9977/10000, exists and is
    accepted by his unmodified interval verifier on all 201 directions, so that
    s(82) >= 93/10 by his continuous covering argument, and hence s(n) >= 93/10 for every
    n >= 82, which moves the verified rows for n = 82, 83, 84 and 85.
  lane: proof
  derived_from: [X-039]
  criterion:
    shape: determination
    metric: >-
      An accepting run_verify.py replay of the ladder's highest frozen certificate at
      or above side 93/10, its exact mass recomputed and strictly below 82, and the
      exact-rational preflight of the interval input, all on the published bytes
    direction: >-
      Confirm only on the accepting replay plus the preflight, never on push.py's own
      status. The ladder giving up below 93/10 is a bounded negative about this driver
      from the trivial seed; any accepted rung above 1 + sqrt(65) = 9.062 is still a
      candidate row. A register row waits for a Fable max W2 review through the
      wand125-format intake.
    threshold: 93/10
  instrument: >-
    tokoharu/square-packing-density-bounds push.py from its trivial seed, pinned at
    84bebef, one search worker and two verify workers; admission through the
    generalised devtools.audit_tokoharu_density preflight and run_verify.py
  instrument_ready: true
  regime: >-
    n=82; rectangle densities D4-symmetrized about the centre; 201-direction rational
    angle net; outward-rounded interval verification
  instance: {axis: n, point: 82}
  priority: 1
  cost_estimate: >-
    Launcher only; one night of one search worker plus two verify workers; per-rung
    cost read from the first rungs
  prereqs: [think-pr2b]
  replication: false
  registered: '2026-09-27'
  notes: >-
    From the 2026-09-27 planning block
    (docs/project/specs/archive/plan-2026-09-27-after-4640020-overnight.md). wand125's
    rectangle certificates stop at n = 78, so n = 82..97 stay at Nagamochi's closed forms
    1 + sqrt(n - 17), against reported packings from 9.5355 to 10; the gap at n = 82 is
    0.47. A certificate at 9.3 lifts n = 82..85; one at 9.5 would lift n = 82..89. X-039
    listed 82..97 among the ranges where a first-party certificate would move the
    register.
---
# H-251: The Widest Verified Gap Below n = 100

Nagamochi’s $1+\sqrt{n-17}$ is the whole of what is verified for n = 82 to 97, about
half a unit under the reported packings.
One rectangle certificate at n = 82 covers every larger n by mass, so the first rung
above $9.062$ moves several rows at once.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
