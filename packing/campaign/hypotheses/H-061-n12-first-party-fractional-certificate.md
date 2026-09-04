---
title: H-061 — a first-party fractional certificate proves s(12) ≥ 19/5
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-061
  kind: hypothesis
  claim: >-
    There is a finite measure of rational-weight point atoms in [0, 19/5]^2 with total
    mass strictly below 12 such that every closed unit square contained in [0, 19/5]^2,
    at every orientation, captures mass at least 1; hence s(12) >= 19/5 = 3.8, the
    first lower bound specific to n = 12, above the inherited 2 + 4/sqrt(5) =
    3.788854... that Stromquist's n = 11 argument supplies by monotonicity.
  lane: proof
  derived_from: [X-010, X-011]
  strategy_refs: ['proof:17', 'proof:21', 'proof:22']
  criterion:
    shape: determination
    metric: >-
      an exact certificate at side 19/5 and n = 12, replayed by the repository's
      general event-cell verifier over a declared finite rational direction set with
      the shrink-and-scaling lemma covering every intermediate orientation
    direction: >-
      accepted only if the frozen verifier accepts the rationalised certificate from a
      clean output root under normal and optimized Python, an independent reviewer
      replays it and re-derives the decision from the emitted bytes with a from-scratch
      evaluator, and the lemma chain (closed versus open squares, shrink and scaling,
      strictness of total mass below 12, finitely many directions) is audited; rejected
      only by an exact ceiling certificate -- a converged dual re-solved for true unit
      squares and scaled by its exact maximum depth, proving by weak duality that the
      fractional piercing value at side 19/5 is at least 12, so that no such measure
      exists; a restricted optimum at or above 12 - 1/500 on the declared site grid
      without a converged dual is a bounded negative for that grid and leaves the
      hypothesis unresolved
    threshold: exact certificate at side 19/5 with total mass strictly below 12
  instrument: >-
    A first-party generator on the Burns--Massaccesi architecture: an LP over candidate
    atom weights on a declared grid, constrained so that every pose in a growing finite
    pose set captures mass at least 1, with the exact event-cell sweep of the n = 17
    verifier generalised to (n, side, atoms, directions, shrink margin) as the separation
    oracle on the fixed direction set, column generation for atom sites from the dual,
    and rationalisation of the float solution into exact weights with a provable margin.
    Positive controls: the adopted Massaccesi certificate re-encoded in the general
    format, the retained Burns certificate whose row minima are not all 1, the n = 17
    selftest fixtures, and Massaccesi's published generator setting returning a total
    below 17. Limitation control: green17's unit-spaced sixteen points, which the
    shrink verifier refuses at every side by construction and which are retained as
    the method's boundary. Negative controls: total mass reaching n, one atom
    lightened, a dropped bracketing and a dropped interior direction, the shrunken
    side pushed past the containment condition, the certificate at 451/100, an atom
    outside the container, and a broken symmetry, each refused identically under
    optimized Python. Stromquist's ten-point set is not a control: read as a measure it
    has mass exactly eleven and lives in Q(sqrt 5). The instrument is frozen and
    reviewed target-blind before this hypothesis is evaluated.
  instrument_ready: false
  regime: >-
    twelve closed unit squares with pairwise disjoint interiors in the closed square
    [0, 19/5]^2 at every orientation; exact rational arithmetic over Q throughout; the
    finite direction set and shrunken side declared in the certificate and covered by
    the shrink-and-scaling lemma the BC-150 packet writes out -- with 181 directions
    and B = 9973/10000 the certificate is a unit-square certificate at the effective
    side 38000/9973, about 0.0103 above 19/5; no numerical tolerance enters the decision
  instance: {axis: n, point: 12}
  priority: 1
  cost_estimate: >-
    one 135-minute W7 build and freeze, one 85-minute W6 round, and one 45-minute
    independent review inside Agenda 017; LP sizes at n = 12 are far below the n = 17
    certificate's 168 atoms and 181 directions
  prereqs:
  - the general exact event-cell verifier, frozen and reviewed target-blind (BC-160)
  - the two positive controls and three negative controls passing at the frozen revision
  - an independent reviewer with no authorship in the generator (BC-162)
  replication: true
  registered: '2026-09-04'
  notes: >-
    The threshold is fixed here, before any target command runs, as H-039 requires, and
    it does not move after results are seen: a certificate at a lower side is a typed
    result about the generator, recorded and not promoted; a certificate at a higher
    side is registered at its actual side only if 19/5 is also certified, since the
    hypothesis names 19/5. The value was chosen from the uncertified pierce pilot of
    2026-08-31, whose restricted fractional value was about 10.67 at side 3.80, 11.0 at
    3.83 and 12.53 at 3.86 -- neither an upper nor a lower bound on the true value --
    so 19/5 leaves margin below 12 while any success is the first n = 12-specific bound
    in the problem's history -- by 0.011, which the record says plainly. The planning
    survey's own reading confirms the choice: 19/5 exceeds 2 + 4/sqrt(5) exactly, since
    (9/5)^2 = 81/25 > 16/5; at the effective side the pilot interpolates to about 10.8,
    the largest margin of any candidate above the inherited bound; and the value is
    inside the window the Lane A3 bead named. Later rungs (383/100, 77/20, 97/25 --
    which would separate s(12) from Trump's side -- 39/10, 79/20) are separate
    hypotheses registered one at a time at Agenda 018's preflight. A certificate at
    side 4 itself with mass below 12 would prove s(12) = 4 outright, since the scaling
    lemma needs only a strictly smaller side. A success is previously-published
    in architecture and first-party in the certificate; it claims V4/C3 at most, one
    method family, and never C4. The same certificate at any side above 2 + 4/sqrt(5)
    with total mass strictly below 11 would improve s(11); that is H-063's separate
    claim and is not this one.
---
# H-061 — A First-Party Fractional Certificate Proves `s(12) ≥ 19/5`

Twelve squares are easier to pack than thirteen, so `s(12) = 4` is a strictly stronger
statement than Bentz’s proved `s(13) = 4`, and nothing specific to `n = 12` has ever
been proved: the standing lower bound is Stromquist’s `n = 11` bound inherited by
monotonicity. The fractional unavoidable-set architecture that Burns and Massaccesi
published at `n = 17`, and that this repository replayed with five implementations and
adopted as `T-015`, has never been aimed at `n = 12`. A measure of total mass below
twelve that every unit square captures at least one unit of is a certificate that no
twelve disjoint unit squares fit, and the side at which such a measure exists is a lower
bound.

The claim fixes the side at `19/5` so that the round can be wrong.
The uncertified pilot suggests the fractional window at `n = 12` closes somewhere near
`3.85`; `19/5` sits inside it with margin, and the ladder above it is registered one
rung at a time rather than by moving this threshold.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
