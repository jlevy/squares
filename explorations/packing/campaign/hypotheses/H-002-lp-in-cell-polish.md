---
title: H-002 — LP-in-cell polish is exact and sufficient
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-002
  kind: hypothesis
  claim: >-
    Alternating per-cell LP solves with local angle moves refines any annealer output to
    a genuine cell-optimum whose side matches the analytic value to LP precision on
    solved cases.
  lane: search
  derived_from: [X-001]
  strategy_refs: ['search:17', 'search:19']
  criterion:
    shape: record
    metric: best_side
    direction: lower
    threshold: 1e-12 against the analytic value
  instrument: >-
    Built: sqpack/quench.py and run_quench.py. A scipy HiGHS LP solves a fixed-angle,
    fixed-axis cell; the quench re-reads the cell and uses local angle descent or
    class-bracketing search.
  instrument_ready: true
  regime: annealer outputs at n = 5, 10, 11; LP values are numerical screens, not certificates
  instance: {axis: n, point: 11}
  sweep: {axis: n, points: [5, 10, 11]}
  priority: 1
  cost_estimate: tier M (five seeds, up to 30 s per quench)
  prereqs: []
  replication: false
  registered: retroactive
  notes: >-
    Refuted as a universal claim by exp-006 and exp-009. The fixed-cell LP reproduces
    the n = 11 reference at its supplied angles to 4.4e-16, and class-bracketing reaches
    machine precision from the tested annealer outputs at n = 5 and n = 10 (exp-007 and
    exp-008). At n = 11 the same local procedure remains 6.29e-02 above the standing
    best (exp-009). This supports a local polishing and diagnostic role, not global
    convergence or a unique basin identity.
---
# H-002 — LP-in-cell polish is exact and sufficient

The original universal claim is **refuted**. The implemented quench is valuable in a
narrower role: it gives a numerical local refinement and shows when a tested start
remains far above the target after that refinement.
It does not make basin identity canonical, does not cross basin boundaries, and does not
replace certification.

On the tested annealer outputs, class-bracketing reaches the analytic values to machine
precision at `n = 5` and `n = 10`
([exp-007](../series/series-000-smoke-and-calibration/experiments/exp-007-quench-bracket-n5.md)
and
[exp-008](../series/series-000-smoke-and-calibration/experiments/exp-008-quench-bracket-n10.md)).
At `n = 11`, it remains `6.29e-02` above the standing best
([exp-009](../series/series-000-smoke-and-calibration/experiments/exp-009-quench-bracket-n11.md)).
For these tested starts, the contrast distinguishes a residual the quench can remove
from one it cannot; it does not prove that the latter start lies in a different basin or
establish a global landscape partition.

## The result this rests on is already verified

For fixed angles, and with each pair’s separating axis fixed, minimising `s` is a
**linear program**: corners are affine in centres, the separating-axis conditions are
linear inequalities, containment is linear, the objective is linear.
All of this problem’s nonconvexity lives in the angles and in the combinatorial choice
of cell.

The fixed-cell solve was independently reproduced in
[exp-006](../series/series-000-smoke-and-calibration/experiments/exp-006-lp-quench-n5-n10-n11.md):
at the supplied angles of the standing `n = 11` packing it returns a side within
`4.4e-16` of the reference.
This is a solver-precision numerical result for that supplied cell, not an algebraic
certificate or evidence that all starts with those angles reach that cell.

## Why this campaign needs it specifically

[exp-001](../series/series-000-smoke-and-calibration/experiments/exp-001-baseline-sweep.md)
found a near-optimal `n = 10` start.
Class-bracketing then reached the proved analytic value on the tested outputs, whereas
finite-difference descent did not.
In contrast, the `n = 11` outputs tested in
[exp-006](../series/series-000-smoke-and-calibration/experiments/exp-006-lp-quench-n5-n10-n11.md)
and
[exp-009](../series/series-000-smoke-and-calibration/experiments/exp-009-quench-bracket-n11.md)
remain far from the standing best after local polishing.
A quench can therefore screen and sharpen a candidate before the exact layer, but only
the exact verifier can certify it and the quench does not solve the problem of proposing
the right basin.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
