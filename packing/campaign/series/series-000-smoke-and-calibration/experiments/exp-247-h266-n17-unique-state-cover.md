---
title: "exp-247 \u2014 n17 unique-state capacity-one cover"
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-247
  series: series-000
  title: A 24-cell D4-symmetric capacity-one n17 cover with the endpoint family in a unique state
  date: '2026-10-02'
  hypotheses:
  - H-266
  tier: confirmatory
  subject:
    label: The design ring-3-voronoi-8-tabbed-unique, with corners of side 79/100, side cells S1 of depth
      93/100 and width 257/375 and S0, S2 of depth 911/1000 and width 529/750, eight interior Voronoi cells
      cut at S1's top and below a chord, and the H256 endpoint family over a proved superset of its slider
      range.
    engine: devtools.check_n17_capacity_one_cover with the unique_state check, and an independent review that
      recomputed the wall lemma, diameters, coverage, D4 count and family distances in separate code
    assurance: verified
    method: exact-algebraic
    host_system: Linux x86_64 remote session container, project Python 3.14.7, one worker
    selftest_passed: true
    engine_commit: 0dabde12900fd5f1c6393fe5171f13c41672da73
  instance:
    axis: n
    point: 17
    role: target
  method:
    control: The H259 falsifier pair, a diameter-1 cell, inadmissible wall cells, a removed cell, a shallower
      ring and a perturbed cell are refused; the exp-246 tabbed design fails unique_state on squares 13 and 11.
      Nineteen tests, ruff and BasedPyright clean.
    candidate: Exact rational cells; capacity by interior diameter or the depth-width wall lemma; exact
      coverage; D4 invariance and Burnside; one assigned state with every family centre at least 1e-3 inside
      its cell and outside every other cell.
    runs_per_condition: 1
    interleaved: false
    operator: Claude Session 168; lane G2 built the design in Session 167, the coordinator ran it from a clean
      worktree
    entry_point: packing/devtools/check_n17_capacity_one_cover.py
    command: 'From packing: .venv/bin/python3 -m devtools.check_n17_capacity_one_cover --design
      ring-3-voronoi-8-tabbed-unique --output FILE. Exact line in run-001 command.txt.'
    budget: The check runs in about a second on one worker.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/exp-247-n17-unique-state-cover/run-001
    dirty: false
    commit: 37b5fc2ffb15ecda20b77e4a8a375eff9c212397
  results:
  - shape: determination
    role: outcome
    question: Is the design a D4-symmetric capacity-one cover with N <= 25, holding the endpoint family in one
      unique state with margin at least 1e-3?
    outcome: criterion_met
    checked_by: 24 cells; wall-cell maxima -0.0034802 (S1), -0.0035253 (S0, S2) and -0.0115261 (corners) by the
      review's separate exact method; interior squared diameters at most 0.969569; union area exactly
      (U-1)^2 with no positive-area triple overlaps; 43,593 orbits by Burnside and by brute force over all
      346,104 states; the family in one state, unique, least margin 0.002112 (square 13 against side-S1's top).
  - shape: determination
    role: guard
    question: Do the controls, the square-6 scope and the independent review hold?
    outcome: criterion_met
    checked_by: Controls refused; the declared square-6 box is a proved superset of H256's range; the
      independent review finds no blocking defect.
  verdict:
    decision: accepted
    primary_criterion: N <= 25 with every item exact or outward, the family in one state with margin at least
      1e-3, synthetic controls, and an independent review of the depth-width wall lemma.
    reason: Every criterion item holds for the unique-state design, which keeps the 43,593-orbit census. The
      exp-246 tabbed design stays unresolved; this round supersedes it for H-266.
    needs_review: false
    commit: 0dabde12900fd5f1c6393fe5171f13c41672da73
  effort:
    timebox: 120 seconds; one worker
    wall_seconds: 1.0
    stopped_by: criterion
---
# exp-247: A Unique-State Capacity-One Cover for n17

[exp-246](exp-246-h266-n17-capacity-one-cover.md) certified a 24-cell cover but left
[H-266](../../../hypotheses/H-266-n17-minimal-capacity-one-cover.md) unresolved: the
endpoint family realised a second state through an overlapping cell.
Session 167’s lane G2 added a `unique_state` check and redesigned the ring so that
square 13 sits in a deeper, narrower side cell and square 11 stays out of the diagonal
cell.

## Outcome

The redesigned cover satisfies every item of the frozen criterion.
The
[independent review](../../../../../docs/project/reviews/review-2026-10-02-n17-unique-state-cover.md)
recomputed every item in separate code, by different exact methods, and found no
blocking defect. Its scripts are retained under
[`audit/`](../results/exp-247-n17-unique-state-cover/audit/). The n17 census on this
cover is 43,593 D4 orbits, against 7,703,312 on the H259 grid after its free cuts.

The review records one mismatch outside H-266: the local theorem’s declared slider box
reaches $z=1/16$, where square 13 crosses its cell’s top.
The capture step works inside this state, so square 13’s cell bounds $z$ well below
that.
[H-268](../../../hypotheses/H-268-n17-local-theorem-slider-coverage.md) carries the
remaining slide bounds.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
