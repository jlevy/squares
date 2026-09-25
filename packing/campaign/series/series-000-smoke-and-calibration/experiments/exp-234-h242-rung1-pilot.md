---
title: exp-234 — pricing rung 1 with eighteen boxes away from Trump's tilt
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-234
  series: series-000
  title: Pricing rung 1 with eighteen boxes away from Trump's tilt
  date: '2026-09-24'
  hypotheses: [H-242]
  tier: exploratory
  subject:
    label: >-
      The rung-0 fixed-angle cell tree, unchanged except for the reviewed box preset, on
      eighteen half-tangent boxes of the six-axis plus five-common-angle family at tilts
      6, 13, 20, 27, 33 and 43.5 degrees and widths 1e-4, 1e-3 and 1e-2, target U, each
      split into subtrees with a node cap of 150,000 per subtree, and the independent
      reader on every tree
    engine: >-
      packing/cases/trump11/fixed_angle_tree.py box preset (git hash-object 42d52c38,
      admitted by a W2 review) and the unchanged reader fixed_angle_tree_check.py
      (c4ae4e48)
    assurance: verified
    method: exact-algebraic
    host_system: macOS, Claude Session 158; project Python 3.14.7; 9 workers
  instance: {axis: n, point: 11, role: target}
  method:
    control: >-
      The preset's 4+1 controls (close at 27/10, open at 3001/1000, tampering refused) and
      h236 byte-identity; no box contains Trump's tilt, so no local theorem applies
    candidate: >-
      Per box, the reader's verdict, unresolved reasons, leaf certificates and the
      producer's node count and closed measure, read from the reader's statement.
    runs_per_condition: 1
    interleaved: false
    operator: Claude Session 158 coordinator
    entry_point: packing/cases/trump11/fixed_angle_tree.py
    command: >-
      attic/rung1-pilot/run-pilot.sh (retained in exp-234-h242-pilot-receipts.tar.gz):
      for each box, fixed_angle_tree box --t-lo L --t-hi H --strong 6 --node-cap 150000
      --wall-cap 1000000000 --workers 9, then the reader; narrowest widths first
    budget: >-
      About five hours; node caps only, so a laptop sleep would delay rather than
      truncate. The first launch used 8,000,000 per subtree and was stopped before any box
      completed, because the cap is per subtree (logged in pilot.log).
    record: packing/campaign/series/series-000-smoke-and-calibration/results/agenda-042/
  effort:
    timebox: 150,000 nodes per subtree
    wall_seconds: 11264
    stopped_by: criterion
  results:
  - shape: determination
    role: outcome
    question: >-
      Does the rung-0 tree close boxes away from Trump's tilt at a modest cap, and how
      does its progress depend on width and tilt?
    outcome: no_progress
    checked_by: >-
      No box closed. Every one of the eighteen stopped with between 1,040 and 1,290
      subtree leaves unresolved at the node cap, after 3.49 to 4.04 million nodes and
      3.0 to 3.5 million accepted leaf certificates, with a closed measure between 0.624
      and 0.672. The closed measure does not trend with width (1e-4, 1e-3, 1e-2) or with
      tilt (6 to 43.5 degrees). One box, 43.5 degrees at width 1e-2, also reported one
      open leaf, a feasible point of the core relaxation that the W2 review predicted at
      wide boxes and that is not checked as unit squares; one box, 13 degrees at width
      1e-3, left one leaf unresolved on an LP solve error. The reader's statement
      confirms target U and no Trump image on every box
      (exp-234-h242-pilot-receipts.tar.gz)
  - shape: determination
    role: mechanism
    question: What does the pilot say about the price of H-112?
    outcome: criterion_met
    checked_by: >-
      Cost is set by the fixed-angle centre enumeration, not by the angle box: a box a
      hundred times wider makes the same progress for the same nodes, and moving away
      from Trump's tilt does not make a box cheap. At about two-thirds of the measure
      closed for four million nodes, a box is plausibly of rung 0's order (1.7e8 nodes),
      so rung 1 tiled with boxes of width 1e-2 or wider would need a few dozen boxes of
      that order, which this relaxation cannot reach on one machine
  verdict:
    decision: unresolved
    primary_criterion: >-
      Per-box verdicts and node counts at the declared cap, pricing whether H-112 is a
      tiling computation.
    reason: >-
      No box closed at the cap, so rung 1's total cost is not measured, only bounded
      below; but the flat response to width and tilt shows the cost lives in the
      centre enumeration, so the stronger per-node relaxation, not more or narrower
      boxes, is the prerequisite for H-112, while wide boxes remain usable once it exists.
    resume_from: >-
      exp-234-h242-pilot-receipts.tar.gz holds every summary and reader verdict; the
      trees themselves are in attic/rung1-pilot/run of the Session 158 worktree.
---
# Exp-234: Pricing Rung 1

[H-242](../../../hypotheses/H-242-n11-rung1-pilot-cost-away-from-trump.md) asked whether
boxes away from Trump’s tilt, where the side has a positive margin to $U$, would be much
cheaper than rung 0’s box, which contains Trump’s packing and cost about $1.7\times10^8$
nodes. They are not.
Eighteen boxes across the tilt range, from $10^{-4}$ to $10^{-2}$ wide, all stopped at a
cap of 150,000 nodes per subtree with about two-thirds of their measure closed, after
roughly four million nodes each, and the fraction closed barely moved with width or
tilt.

That answers the pricing question in the direction that matters.
The cost is in the fixed-angle centre enumeration, which is the same at every tilt, so
rung 1 needs a stronger bound per node before it needs anything else.
The one encouraging reading is that width is nearly free: once a node closes faster,
rung 1 can be tiled with a few dozen wide boxes rather than hundreds of narrow ones.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
