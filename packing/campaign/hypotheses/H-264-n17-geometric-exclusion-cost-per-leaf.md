---
title: H-264 — the cost of exact geometric exclusion per n17 occupancy leaf
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-264
  kind: open_question
  claim: >-
    On a seeded stratified draw of residue orbits on the H-266 unique-state cover at cap
    U = 1169/250 (survey_n17_residue's arity8 frame: the 2,256 orbits surviving the 90
    arity-at-most-8 selector flags; draw --sample 12 --seed 182), what fraction does the
    17-owner ownership-induction kernel at 32 bins exclude by a certificate the standing
    kernel verifier re-proves in full, at what producer, checker and verifier cost per
    state, and what does that extrapolate to over the frame's drawn strata?
  lane: proof
  derived_from: [X-048]
  instrument: >-
    devtools.check_n17_subpattern at the session-182 registration commit with N1's
    parameters (--bins 32 --max-rounds 24 --hull-limit 16 --max-seconds 7000, producer
    share 0.5, envelope core, collisions on); closures re-proved by
    devtools.verify_n17_kernel_certificate in full mode under the kernel-closed-covers
    listing or a later one; a float pre-screen by devtools.survey_n17_residue on the same
    draw
  instrument_ready: true
  regime: >-
    n=17; the H-266 unique-state cover at U; cap above S* so exclusions apply to every
    smaller side by the centred embedding. The draws at distance 4 or more from the
    endpoint's state are counted; the distance-2 draws are a declared secondary stratum,
    reported separately because such a state may be feasible at U. A draw the float
    pre-screen places leaves the count and is reported as a candidate near-endpoint state
    pending an exact check. A run that ends at its wall ceiling with process CPU below
    6,300 s is re-run once at the same ceiling and the re-run counts. A draw in N1's orbit
    takes N1's admitted receipt. Strata the draw does not reach (at review time, every
    distance-8-or-more stratum, 430 of 2,256 orbits) are reported as unsampled, not
    extrapolated.
  instance: {axis: n, point: 17}
  priority: 2
  cost_estimate: At most 7,000 s wall per state; with the endpoint control, at most 26 CPU-hours
  prereqs: [H-266, H-267, think-e17c]
  replication: false
  registered: '2026-10-01'
  notes: >-
    Re-scopes think-11ma after the PR 265 route review. The earlier pilot "below the
    certified endpoint" at a candidate cap of 4.67 would cover only sides up to 4.67 and
    leave (4.67, S*) open; the n11 proof excludes every non-captured case at a cap above
    its endpoint. The n11 replay cost about 640 CPU-seconds per nonfield exclusion; n17
    has 136 pairs and 52 variables against 55 and 33. Affordability falsifier: fewer
    than half of the sampled leaves excluded within 2 CPU-hours each. Rewritten in place
    by Session 182's W10 phase (2026-10-05) as an unlanded draft under conventions §7:
    the claim, instrument, regime, cost estimate and prerequisites changed, and
    451154f60 holds the previous text. The falsifier is unchanged: fewer than half of the
    counted draws are excluded within two CPU-hours each, with N1's 7,000 s wall ceiling
    standing in for that limit. The verdict is fixed as soon as the arithmetic determines
    it, and the remaining runs continue for the cost estimate. N1 and F1 (seed 168, the
    44-flag frame) are prior evidence, not part of the count. With seed 182 and sample 12
    the draw is 2 states at distance 2, 7 at 4 and 3 at 6, so 10 are counted. The
    criterion is met at five closures and falsified at six non-closures. The reviewer
    previewed this draw only to validate the command; no outcome was seen.
---
# H-264: What One Geometric Exclusion Costs

A census that cannot be priced cannot be planned.
This draws residue orbits at random from a named frame, so the measured cost
extrapolates over the strata it reaches, and works at a cap above the endpoint, so every
exclusion it makes is reusable in a final proof.

## Instrument and Prior Evidence

The instrument is n11’s kernel adapted to n17 (`devtools/check_n17_subpattern.py` on
`sqpack.hull_kernel`), with every closure re-proved by the standing kernel verifier
before it counts. Session 182 runs it as lane A of the
[n17 overnight plan](../../../docs/project/specs/done/plan-2026-10-05-n17-overnight.md)
(BC-419), after the float pre-screen and a kernel control on the endpoint’s own state,
which must not close.

Two earlier states are prior evidence and not part of the count.
N1 (distance 4, seed 168, the 44-flag frame) closed in 3,723 s of wall under a two-hour
ceiling and was admitted in exp-250. F1 (distance 6, same frame) reached only a
45-minute producer time cap.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
