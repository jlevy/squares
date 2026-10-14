---
title: H-249 — a rectangle-density certificate in tokoharu's format proves s(12) >= 399/100
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-249
  kind: hypothesis
  claim: >-
    A D4-symmetrized rectangle-density certificate in tokoharu's format, with exact
    total mass strictly below 12 at side 399/100 and shrink B = 9977/10000, exists and
    is accepted by his unmodified interval verifier on all 201 directions, so that
    s(12) >= 399/100 by his continuous covering argument. The first target was 397/100
    until Daniel's s(12) >= 15680/3951 = 3.968616 arrived on 2026-09-27.
  lane: proof
  derived_from: [X-047]
  criterion:
    shape: determination
    metric: >-
      An accepting run_verify.py replay (verification_summary.json status VERIFIED, all
      201 angle cases) of the certificate the ladder froze, its exact mass recomputed
      from the rational weights and strictly below 12, and the exact-rational preflight
      of the interval input against the candidate decimals, all on the published bytes
    direction: >-
      Confirm only on the accepting replay plus the preflight, never on push.py's own
      status (DENS-1 in the tokoharu review). The ladder giving up below 3.9687 is a
      bounded negative about the rectangle route at n = 12 with this driver, not about
      s(12). A register row waits for a Fable max W2 review.
    threshold: 399/100
  instrument: >-
    tokoharu/square-packing-density-bounds push.py from its trivial seed, pinned at
    84bebef, in a scratch Python 3.12 environment; admission through
    devtools.audit_tokoharu_density generalised to any certificate directory, and
    run_verify.py
  instrument_ready: true
  regime: >-
    n=12; rectangle densities D4-symmetrized about the centre; 201-direction rational
    angle net with B(1+D) < 1; outward-rounded interval verification
  instance: {axis: n, point: 12}
  priority: 2
  cost_estimate: >-
    Launcher only; about an hour of one worker to climb from the seed to 3.96 at step
    1/50, unknown above it
  prereqs: [think-ujwy]
  replication: false
  registered: '2026-09-27'
  notes: >-
    From the 2026-09-27 planning block
    (docs/project/specs/archive/plan-2026-09-27-after-4640020-overnight.md). A
    fourteen-minute probe from the trivial seed started at 3.3808 and accepted 1/200
    rungs every 60 to 100 s with LP mass 9.009 against budget 12. T-017 holds 3.96;
    the parent-core architecture cannot reach the integer endpoint 4 and the additive
    point route was not shown dead above 3.9609 (H-241), so the rectangle route is the
    untested one at n = 12.
---
# H-249: The Rectangle Route at n = 12

The rectangle-density argument did well next to integer endpoints elsewhere, reaching
$4.985$ at n = 21 against the grid’s $5$. At n = 12 the register holds $3.96$ against
$4$, and no rectangle certificate has been tried.
A ladder from the trivial seed prices it in a night.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
