---
title: exp-229 — a point certificate at n21, side 122/25
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-229
  series: series-000
  title: A point certificate at n21, side 122/25
  date: '2026-09-23'
  hypotheses: [H-240]
  tier: confirmatory
  subject:
    label: >-
      Restricted covering at n=21, side 122/25, B = 9977/10000, the 181-direction net,
      auto grids (34, 46, 56) at inset 1/2, on three site sets: A seeded from the n20
      certificate with six windows, B with five windows, C with no windows; freeze,
      declare the least cell mass, then decide
    engine: >-
      sqpack.fractional.colgen through devtools.run_fractional_colgen;
      declare_least_cell_mass; both routes of decide_certificate, at instrument commit
      69dac09a with no tracked tool changed
    assurance: verified
    method: exact-algebraic
    host_system: macOS, Claude Session 156 lane; project Python 3.14.7; single-process runs, gate at PACK_JOBS=3
  instance: {axis: n, point: 21, role: target}
  method:
    control: >-
      The stock gate's own paired routes; set B's interval refusal on a degenerate seam
      (rows exactly B apart) is the instrument's refusal behaving as designed
    candidate: >-
      Confirm H-240 only on RETAINABLE with mass below 21, followed by a Fable max W2
      review before any register entry; reject the site sets when two converge at 21 or
      above or return the grid.
    runs_per_condition: 1
    interleaved: false
    operator: Claude Session 156, Opus high lane
    entry_point: packing/devtools/run_fractional_colgen.py
    command: >-
      cd packing && uv run --frozen --all-extras --group dev python -m
      devtools.run_fractional_colgen --n 21 --side 122/25 --shrink 9977/10000
      --direction-steps 181 --grid-counts auto --scale 4000000 --support-cap 32
      --column-rounds 1 --max-rounds 80 --deadline-seconds 2700 --seed-windows 0
      --freeze C-covering.json --freeze-family C-family.json --json C-run.json
      --row-log C-rows.jsonl --log C.log; then declare_least_cell_mass and
      decide_certificate on the declared copy (exp-229-n21-run-C.sh)
    budget: One or two runs of at most 3,600 s each, then the gate.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/agenda-042/
  effort:
    timebox: 3,600 s per run
    wall_seconds: 6414
    stopped_by: criterion
  results:
  - shape: determination
    role: outcome
    question: >-
      Does a frozen point certificate at n=21, side 122/25, mass below 21, print
      RETAINABLE from both routes of decide_certificate?
    outcome: criterion_met
    checked_by: >-
      Set C: decide_certificate printed "RETAINABLE: both routes accept and agree at
      250001/250000; sha256
      b230f7cd6806343f115331caf53f02019cc634a8959359684581835a0cc7fb0f"; interval
      enclosure (250001/250000, 250001/250000) over 4,289,657 boxes with 0 stalled in
      67 s; exact route least 250001/250000 in 15 s; 1,228 atoms, mass
      5036431/250000 = 20.145724. Set B converged at mass 20.132143 but its interval
      route stalled on 1,608 boxes of a degenerate seam and refused; set A reached its
      deadline unconverged
  - shape: record
    role: outcome
    metric: frozen covering mass (exact rational)
    direction: lower
    score: 20.145724
    standing_best: 21
    standing_best_source: H-240 criterion (mass strictly below 21)
    beat_record: false
    runs: 3
  verdict:
    decision: accepted
    primary_criterion: >-
      RETAINABLE from both routes on a freeze below mass 21; register only after a
      Fable max W2 review.
    reason: >-
      Both routes accept set C's certificate at least cell mass 250001/250000 with total
      mass 20.145724 < 21, so the gate certifies the covering at side 122/25; the claim
      s(21) >= 122/25 is registered only after the W2 review the hypothesis requires.
---
# Exp-229: A Point Certificate at n21, Side 122/25

[H-240](../../../hypotheses/H-240-n21-additive-certificate-at-4-88.md) was X-047’s one
low case with real additive headroom.
Of three site sets, the plainest one — auto grids with no seed and no windows —
converged in eleven minutes and passed both routes of the gate at mass $20.1457$, so the
covering holds at $122/25=4.88$ against the verified $4.85$. The
[receipt](../results/agenda-042/exp-229-n21-122-25-receipt.md) records all three sets,
including set B’s refusal: its window lattice put atom rows exactly $B$ apart, and the
interval route stalled on the seam where an upright square has both closed edges on such
a pair. That is a refusal, not a counterexample, and set C has no such pair.

Registering the bound waits for the Fable max review H-240 names.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
