---
title: "exp-248 — n17 slide coverage and the local theorem on the widened box"
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-248
  series: series-000
  title: Slide bounds from the endpoint's occupancy state, and the local theorem over the box they need
  date: '2026-10-02'
  hypotheses:
  - H-268
  tier: confirmatory
  subject:
    label: Packings in the endpoint's occupancy state on the H-266 unique-state cover with their 45 non-slider
      coordinates within 1/5000 of the family (run-001), and the local minimum modulo sliders over
      B_W' = [0,1/4] x [-1/2500,1/12] x [-1/8,1/16] (run-002).
    engine: devtools.check_n17_slider_coverage at 05b078bd and devtools.check_n17_local_minimum at 9c26793c,
      with an independent review of both and of their composition
    assurance: verified
    method: exact-algebraic
    host_system: Linux x86_64 remote session container, project Python 3.14.7, one worker
    selftest_passed: true
    engine_commit: 9c26793c157cf52c2f202d5d4b2162e8b4a31328
  instance:
    axis: n
    point: 17
    role: target
  method:
    control: Slide coverage refuses square 6 unconfined, square 13 deleted and square 9 deleted. The local
      theorem refuses a flipped branch, a perturbed slope, a negative dual vertex, an over-large radius, a
      positive corner choice, a restored 9/11 face and a tampered H-257 certificate, and replays n11's worst
      ratio 0.676505 exactly.
    candidate: Exact separating-axis and containment bounds with outward intervals over the root box and a
      branch and bound over square 6's pose and the slide domains; then the exp-244 certificate items over the
      box that contains the certified slides.
    runs_per_condition: 1
    interleaved: false
    operator: Claude Session 168; lanes H, H2 and A3 built the tools, the coordinator ran both from a clean
      worktree
    entry_point: packing/devtools/check_n17_slider_coverage.py
    command: 'From packing: .venv/bin/python3 -m devtools.check_n17_slider_coverage --output FILE (run-001);
      .venv/bin/python3 -m devtools.check_n17_local_minimum --ratio --box 0 1/4 -1/2500 1/12 -1/8 1/16 --output
      FILE --certificates FILE (run-002). Exact lines in each run''s command.txt.'
    budget: Seconds per run on one worker.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/exp-248-n17-local-half-composition
    dirty: false
    commit: f8c1246b2e6ddf53fd76a6a2f9c5ad060579e081
  results:
  - shape: determination
    role: outcome
    question: With square 6 in its cover cell and the other non-slider coordinates within 1/5000, do the slides
      stay inside a box over which the local theorem holds?
    outcome: criterion_met
    checked_by: a in [0, 23/200], b in [b*, 37/500] with b* = -1.684957 r, z in [-49/1000, 0.0241004], so
      a <= 1/4, z >= -1/8 and b <= 1/12 hold with strict margin; the local theorem passes over B_W', which
      contains the certified slides, at r = 1/5000 on 93 cells with worst ratio 0.925931. The independent
      review proved the separation lemma and found it sharp, and recomputed b* and z* in separate code.
  - shape: determination
    role: guard
    question: Does the claim's stated consequence hold as written?
    outcome: criterion_missed
    checked_by: The claim says the certified box B_W contains the slider coordinates. b >= 0 does not follow,
      because the 9/11 contact allows b down to b*, so the box is B_W', and the local theorem was re-run over
      it in run-002. This is a recorded deviation in the consequence, not in the frozen criterion's
      thresholds.
  verdict:
    decision: accepted
    primary_criterion: Strict margins on a <= 1/4 and z >= -1/8 (and b <= 1/12), with synthetic controls and an
      independent review.
    reason: Every criterion item holds with strict margin, and the composition with the B_W' local theorem
      and the H-266 cover gives the capture-target theorem. The deviation is recorded; H-261, whose claim
      names the whole physical slider domain, stays unresolved.
    needs_review: false
    commit: 05b078bd055b6fd901adeaa329b01c7311a12c24
  effort:
    timebox: 900 seconds per run; one worker
    wall_seconds: 27.4
    stopped_by: criterion
---
# exp-248: n17 Slide Coverage and the Local Theorem on the Widened Box

[H-268](../../../hypotheses/H-268-n17-local-theorem-slider-coverage.md) asked whether
square 6’s cover cell keeps the sliding squares inside the box where the local theorem
holds. [exp-244](exp-244-h261-n17-local-minimum.md) certified that theorem on a declared
box but could not say every relevant packing stays in it.

## The Composed Theorem

The
[composition review](../../../../../docs/project/reviews/review-2026-10-02-n17-local-half-composition.md)
states what the two runs and the H-266 cover prove together.
Take a packing $P$ of 17 unit squares in $[0,S]^2$ with $S\le S^\ast$, with its
lower-left corner placed at the family’s concentric corner in the cover frame.
Suppose:

- its occupancy state on the
  [unique-state cover](exp-247-h266-n17-unique-state-cover.md) is the endpoint’s, which
  labels its squares;
- in that labelling, its 45 non-slider coordinates are each within $1/5000$ of the
  family’s.

Then its slides lie in $B_W'$, its sixteen squares other than square 6 lie on the
family, and $S=S^\ast$. This is the theorem the capture step must reach.

It leaves three obligations for the global half:

- read the occupancy state in this frame;
- capture to radius $1/5000$ at a cap within about $10^{-12}$ of $S^\ast$;
- charge the rational enclosure of the slide direction to the capture radius.

## Deviation and Scope

H-268’s claim names the exp-244 box $B_W$, but the 9/11 contact lets square 11 move
$1.68r$ toward square 9, so the box used is
$B_W'=[0,\tfrac14]\times[-\tfrac1{2500},\tfrac1{12}]\times[-\tfrac18,\tfrac1{16}]$,
certified in run-002.
[H-261](../../../hypotheses/H-261-n17-local-minimum-modulo-sliders.md) stays unresolved.
The review exhibits a packing at side $S^\ast$ that meets every H-261 premise outside
$B_W'$: the family with squares 5 and 6 exchanged.
Confirming H-261 as worded would be a different theorem, and narrowing its claim would
be a retune.

The review’s scripts are retained under
[`audit/`](../results/exp-248-n17-local-half-composition/audit/).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
