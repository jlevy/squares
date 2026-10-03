---
title: "exp-246 — n17 minimal capacity-one cover"
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-246
  series: series-000
  title: A 24-cell D4-symmetric capacity-one cover of the n17 centre box at cap 1169/250
  date: '2026-10-02'
  hypotheses:
  - H-266
  tier: confirmatory
  subject:
    label: Four corner cells of side 39/50, twelve side cells of depth 911/1000 and width 529/750, eight
      interior Voronoi cells of rational sites with the four axis cells tabbed; the H256 endpoint family over
      a declared box containing its slider triangle.
    engine: devtools.check_n17_capacity_one_cover, with an independent proof review of the depth-width wall
      lemma that re-derived the checked quartic and searched for counterexamples
    assurance: verified
    method: exact-algebraic
    host_system: Linux x86_64 remote session container, project Python 3.14.7, one worker
    selftest_passed: true
    engine_commit: e1f8b14b455da0ae018eeee5727c9aaa6a7c82d9
  instance:
    axis: n
    point: 17
    role: target
  method:
    control: The H259 falsifier pair, a diameter-1 cell, two inadmissible wall cells, a removed cell, a
      shallower ring and a perturbed cell are all refused. The untabbed design is refused because squares
      11 and 13 straddle seams. Sixteen tests, ruff and BasedPyright clean.
    candidate: Exact rational cells; interior squared diameters below 1; the depth-width wall lemma's
      quartic negative on [0,1] by Bernstein coefficients with an agreeing Sturm count; exact slab-sweep
      coverage; D4 invariance and Burnside; endpoint margins in outward interval arithmetic.
    runs_per_condition: 1
    interleaved: false
    operator: Claude Session 167; lane G built the instrument, the coordinator ran it from a clean worktree
    entry_point: packing/devtools/check_n17_capacity_one_cover.py
    command: 'From packing: .venv/bin/python3 -m devtools.check_n17_capacity_one_cover --design
      ring-3-voronoi-8-tabbed --output FILE. Exact line in run-001 command.txt.'
    budget: One build and review slice; the check runs in under a second.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/exp-246-n17-capacity-one-cover/run-001
    dirty: false
    commit: 603d5cb36ed3c9195513956cd5b5c20e5f2cddda
  results:
  - shape: determination
    role: outcome
    question: Is the 24-cell cover a D4-symmetric closed cover of capacity-one cells, and how many orbits
      does it leave?
    outcome: criterion_met
    checked_by: Every cell has capacity one (interior diameters at most 0.98824; side cells max G between
      -0.004663 and -0.002578, the review's exact maximum -0.0035253; corner cells -0.0253242 by the
      one-wall lemma and -0.104020 by the two-wall form); coverage exact; D4 invariant; 346,104 states and
      43,593 orbits by Burnside, 177 times below the cut H259 count. The proof review found the lemma
      correct for every orientation and sharp.
  - shape: determination
    role: guard
    question: Does the whole H256 endpoint family lie in one occupancy state with margin at least 1e-3?
    outcome: criterion_missed
    checked_by: An assignment holding the family exists, with least margin 0.013770 to the seams of the
      assigned cells. Under the existential convention the family also realises a second state, because
      square 13 sits 0.0023 inside the overlapping side cell S1, so capture would face two states. Square
      6's domain is declared rather than derived from H256.
  verdict:
    decision: unresolved
    primary_criterion: N <= 25 with every item exact or outward, the family in one state with margin at
      least 1e-3, synthetic controls, and an independent review of the depth-width wall lemma.
    reason: The cover itself is certified and the lemma reviewed, so the census of 43,593 orbits stands. The
      single-state purpose of the claim is not met while square 13 also lies in side cell S1, and square 6's
      domain is declared. Moving the tab or shrinking S1 by a few thousandths, and deriving square 6's range,
      would close both.
    needs_review: false
    commit: e1f8b14b455da0ae018eeee5727c9aaa6a7c82d9
  effort:
    timebox: 60 seconds; one worker
    wall_seconds: 0.77
    stopped_by: criterion
---
# exp-246: A Minimal Capacity-One Cover for n17

[H-266](../../../hypotheses/H-266-n17-minimal-capacity-one-cover.md) asked for a
D4-symmetric cover of the n17 centre box by at most 25 capacity-one cells that keeps the
endpoint family in one occupancy state.
The
[bulk-exclusion design](../../../../../docs/project/reviews/review-2026-10-02-n17-bulk-exclusion-design.md)
proposed a 24-cell design.
Lane G certified it exactly, adding small tabs to the axis cells so that squares 11 and
13 stay inside them as they slide.
The
[wall-lemma review](../../../../../docs/project/reviews/review-2026-10-02-n17-depth-width-wall-lemma.md)
proved the depth-width lemma the wall and corner cells rely on, and found it sharp.

## Outcome

The cover stands. Each of its 24 cells holds at most one centre, the cells cover the
centre box exactly, and the cover has D4 symmetry.
It leaves 346,104 states and 43,593 D4 orbits, against 7,703,312 on the H259 grid after
its free cuts.

The verdict is unresolved for two closable reasons.
The cells overlap, and under the existential assignment convention the endpoint family
realises a second state: square 13 sits $0.0023$ inside side cell S1 as well as in its
own axis cell. No sound engine can exclude that second state, so capture would face two
cases unless the next design makes the state unique.
Separately, square 6’s range is declared rather than derived from H256. The review
suggests a `unique_state` check that requires every centre to be at least $10^{-3}$
outside every other cell.

The review’s scripts and outputs are retained under
[`audit/`](../results/exp-246-n17-capacity-one-cover/audit/).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
