---
title: "exp-244 — n17 local minimum modulo sliders"
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-244
  series: series-000
  title: Focused-rectangle ratio test modulo the slider cone at r = 1/5000 over a declared slider box
  date: '2026-10-02'
  hypotheses:
  - H-261
  tier: confirmatory
  subject:
    label: The 52 positively weighted H-258 rows at the moving base point x*(w) over B_W = [0,1/4] x [0,1/12]
      x [-1/8,1/16] in the slide parameters (a,b,z), at the exp-237 root-box midpoint with the root-box
      residual folded into epsilon; uniform radius 1/5000 in the 45 non-slider coordinates.
    engine: devtools.check_n17_local_minimum --ratio, with an independent review that rebuilt the rows,
      curvature constants, option margins and the binding certificates in separate code
    assurance: verified
    method: exact-algebraic
    host_system: Linux x86_64 remote session container, project Python 3.14.7, one worker
    selftest_passed: true
    engine_commit: e91bd8597aadf47031062adda56c7cdedfd915f5
  instance:
    axis: n
    point: 17
    role: target
  method:
    control: Seven controls refused (flipped tau branch, perturbed slope, negative dual vertex, radius 3/5000
      failing at ratio 2.78, a positive corner choice, the restored 9/11 face failing slide invariance, a
      tampered H-257 certificate), and n11's own duals replayed through the same ratio routine reproduce
      n11's worst ratio 0.676505208203 exactly. Thirty-five tests, ruff and BasedPyright clean.
    candidate: Per-cell affine duals rounded to 2^-44 and verified exactly, replayed LP-free from JSON; exact
      curvature constants; Taylor margins for the 125 unavailable options of the 19 retained pairs; the
      H-258 stress recomputed along the family.
    runs_per_condition: 1
    interleaved: false
    operator: Claude Session 167; lanes A2-build and A2-build-2 built the instrument, the coordinator ran it
      from a clean worktree
    entry_point: packing/devtools/check_n17_local_minimum.py
    command: 'From packing: .venv/bin/python3 -m devtools.check_n17_local_minimum --ratio --output FILE
      --certificates FILE. Exact line in run-001 command.txt.'
    budget: One build and review slice; target run seconds on one worker.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/exp-244-n17-local-minimum/run-001
    dirty: false
    commit: 603d5cb36ed3c9195513956cd5b5c20e5f2cddda
  results:
  - shape: determination
    role: outcome
    question: Do the kernel, the 90 duals, the curvature bounds, the unavailable options, the stress and
      the ratio test all hold over the declared slider box at r = 1/5000?
    outcome: criterion_met
    checked_by: Kernel of the 52 positive rows exactly the six slider directions at the midpoint and at all
      eight vertices of B_W; all 90 signed non-slider coordinates pass M_j < 2(r_j - eps_j R) on 93 cells,
      worst 0.925818 for -omega_11; all 125 retained unavailable options strictly negative, least -0.055273;
      stress along the family nonnegative, least 0.0042558, six zeros exact. The independent review
      reproduced every curvature constant, every option margin and all four -omega_11 cells exactly.
  - shape: determination
    role: guard
    question: Does the certified box cover the physical slider domain the frozen claim names, and do the
      certified items match the frozen criterion?
    outcome: criterion_missed
    checked_by: With square 6 free, square 5 can slide up to a = 1.074 and square 13 down to z = -0.9165,
      outside B_W, so the claim's "anywhere in the physical slider domain" is not established. The criterion
      names 135 unavailable alternatives; the instrument checks the 125 of the 19 retained pairs, because
      the ten options of the dropped pairs 2/3 and 9/11 constrain nothing the theorem uses (all 135 are
      negative at x*(0) in the point receipt).
  verdict:
    decision: unresolved
    primary_criterion: Every listed item certified exactly or by outward intervals, synthetic controls, and
      an independent maximum-effort review of the composition with no blocking defect.
    reason: The mathematics, instrument and certificates have no blocking defect, and the local minimum
      modulo sliders is certified on the declared box B_W at r = 1/5000. The frozen claim covers the whole
      physical slider domain, which B_W does not, so H-261 as worded is neither confirmed nor refuted.
      Closing it needs a capture-side lemma that a <= 1/4 and z >= -1/8 whenever square 6 lies in its
      occupancy cell, or a wider box.
    needs_review: false
    commit: e91bd8597aadf47031062adda56c7cdedfd915f5
  effort:
    timebox: 600 seconds; one worker
    wall_seconds: 15.2
    stopped_by: criterion
---
# exp-244: n17 Local Minimum Modulo Sliders

[H-261](../../../hypotheses/H-261-n17-local-minimum-modulo-sliders.md) is the local half
of an n17 optimality proof.
It says that near the known packing nothing has a smaller side, with the slider
coordinates of squares 5, 11 and 13 left free and square 6 dropped.
The
[recipe review](../../../../../docs/project/reviews/review-2026-10-02-n17-local-theorem-recipe.md)
fixed the theorem, its lemmas and twelve certification items.
Two Opus lanes built the instrument, and the
[independent review](../../../../../docs/project/reviews/review-2026-10-02-n17-local-theorem-instrument.md)
read the composition and recomputed its numbers in separate code.

## What Is Certified

Every feasible configuration of the sixteen squares other than square 6, in the fixed
container at the exact H255 root, whose 45 non-slider coordinates lie within $1/5000$ of
the endpoint’s and whose slides satisfy $a\in[0,\tfrac14]$, $b\in[0,\tfrac1{12}]$ and
$z\in[-\tfrac18,\tfrac1{16}]$, lies on the endpoint family.
No packing of smaller side embeds there.
The worst ratio is $0.925818$, for $-\omega_{11}$. The independent review reproduced it
from its own rows to within the root-box term.

## Why the Verdict Is Unresolved

H-261’s frozen claim allows the slider coordinates anywhere in the physical slider
domain. Because square 6 is dropped, nothing in the theorem stops square 5 sliding to
$a\approx1.07$ or square 13 to $z\approx-0.92$, both outside the certified box.
This session does not retune the claim after seeing the result.
In a real packing square 6 is present, so the capture step can supply the missing bound.
It must show that $a\le\tfrac14$ and $z\ge-\tfrac18$ whenever square 6 lies in its
occupancy cell of the
[H-266 cover](../../../hypotheses/H-266-n17-minimal-capacity-one-cover.md).
Alternatively, the box can be widened: cheaply in $a$, expensively in $z$, where the
13/14 face degenerates near $z\approx-0.79$.
[H-268](../../../hypotheses/H-268-n17-local-theorem-slider-coverage.md) registers that
lemma.

The criterion’s 135 unavailable alternatives are checked as 125. That is a recorded
deviation, not a defect: the ten others belong to the two dropped pairs, and the point
receipt shows all 135 negative at the base point.

The review’s retained recomputation is under
[`audit/`](../results/exp-244-n17-local-minimum/audit/).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
