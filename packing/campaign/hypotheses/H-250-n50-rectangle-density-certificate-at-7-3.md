---
title: H-250 — a rectangle-density certificate in tokoharu's format proves s(50) >= 73/10
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-250
  kind: hypothesis
  claim: >-
    A D4-symmetrized rectangle-density certificate in tokoharu's format, with exact
    total mass strictly below 50 at side 73/10 and shrink B = 9977/10000, exists and is
    accepted by his unmodified interval verifier on all 201 directions, so that
    s(50) >= 73/10 by his continuous covering argument.
  lane: proof
  derived_from: [X-039]
  criterion:
    shape: determination
    metric: >-
      An accepting run_verify.py replay of the ladder's highest frozen certificate at
      or above side 73/10, its exact mass recomputed and strictly below 50, and the
      exact-rational preflight of the interval input, all on the published bytes
    direction: >-
      Confirm only on the accepting replay plus the preflight, never on push.py's own
      status. The ladder giving up below 73/10 is a bounded negative about this driver
      from the trivial seed, and the highest accepted rung above the register's
      1 + sqrt(37) is still a candidate row. A register row waits for a Fable max W2
      review through the wand125-format intake.
    threshold: 73/10
  instrument: >-
    tokoharu/square-packing-density-bounds push.py from its trivial seed, pinned at
    84bebef, one search worker; admission through the generalised
    devtools.audit_tokoharu_density preflight and run_verify.py
  instrument_ready: true
  regime: >-
    n=50; rectangle densities D4-symmetrized about the centre; 201-direction rational
    angle net; outward-rounded interval verification
  instance: {axis: n, point: 50}
  priority: 1
  cost_estimate: >-
    Launcher only; one night of one search worker plus verify workers; per-rung cost
    read from the first rungs
  prereqs: [think-pr2b]
  replication: false
  registered: '2026-09-27'
  notes: >-
    From the 2026-09-27 planning block
    (docs/project/specs/archive/plan-2026-09-27-after-4640020-overnight.md). n = 50 is
    the one case in 46..61 wand125's rectangle certificates leave at Nagamochi's
    closed form, 1 + sqrt(37) = 7.083 against the reported 7.571; the n = 51 certificate
    at 7.43 has mass 50.99 and does not cover it. X-039 listed 50..61 among the ranges
    where a first-party certificate would move the register.
---
# H-250: The Weakest Row Under n = 62

wand125’s ladder took n = 51 to $7.43$ and left n = 50 at Nagamochi’s $1+\sqrt{37}$. The
same driver from its trivial seed, one worker for a night, prices whether n = 50
follows.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
