---
title: exp-233 — the n12 cutting loop settles below 12 at side 39609/10000
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-233
  series: series-000
  title: The n12 cutting loop settles below 12 at side 39609/10000
  date: '2026-09-24'
  hypotheses: [H-241]
  tier: confirmatory
  subject:
    label: >-
      Second round of H-241: the cutting loop at n=12, side 39609/10000, B = 9977/10000,
      warm-started from exp-230's leg-3 state, with six row rounds of six rows per
      direction and a family support cap of 192
    engine: >-
      devtools.run_fractional_cutting with colgen.check_ceiling at branch commit
      7b4847aa3, no tracked tool changed
    assurance: numerically-checked
    method: numerical-f64
    precision:
      binary_bits: 53
      rounding: nearest-even
    tolerance: >-
      A family counts only when the exact ceiling check proves total over maximum depth
      at least 12; the row loop stops when no placement exceeds depth 1.0000010
    host_system: macOS, Claude Session 157; project Python 3.14.7; single process beside the rung-0 run
  instance: {axis: n, point: 12, role: target}
  method:
    control: exp-230's warm state and settings, changed only in rows per round and support cap
    candidate: >-
      Confirm H-241 on a proved ceiling of at least 12; reject when the loop settles with
      a converged covering value below 12; an unsettled loop decides nothing.
    runs_per_condition: 1
    interleaved: false
    operator: Claude Session 157 coordinator
    entry_point: packing/devtools/run_fractional_cutting.py
    command: >-
      See exp-233-n12-run-leg4.command.txt: run_fractional_cutting --n 12 --side
      39609/10000 --shrink 9977/10000 --angle-limit 207107/500000 --steps 180 --minutes
      345 --iterations 80 --cap 150 --support-cap 192 --rows-rounds 6
      --rows-per-direction 6 --stop-on-covering-below-n --warm <exp-230 leg-3 state>
    budget: 345 minutes on one process.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/agenda-042/
  effort:
    timebox: 345 minutes
    wall_seconds: 7941
    stopped_by: criterion
  results:
  - shape: determination
    role: outcome
    question: >-
      Does the cutting loop at side 39609/10000 prove a depth-one family of total over
      maximum depth at least 12, or settle below 12?
    outcome: criterion_missed
    checked_by: >-
      The loop stopped with "row-converged covering objective below n at iteration 2":
      the covering objective converged at 11.980175 on 19,905 sites and 10,919 rows,
      while the best proved family scaled total was 11.146 and failed K3
      (exp-233-n12-leg4-summary.json)
  verdict:
    decision: rejected
    primary_criterion: >-
      A proved ceiling of at least 12 confirms; a settled covering value below 12
      rejects.
    reason: >-
      The row loop converged with covering value 11.980175 < 12, so no depth-one family
      reaching 12 exists on this support and the additive route at n12 is not shown dead
      above 3.9609; the converged value is a float LP, not a certificate, so it suggests
      rather than establishes a point certificate at 3.9609.
---
# Exp-233: The n12 Cutting Loop Settles Below 12

[H-241](../../../hypotheses/H-241-n12-additive-route-dead-above-3-9609.md) asked for a
decisive negative: a family of cores proving that no additive certificate can reach
$s(12)>3.9609$. The second round, with three times the rows per round and twice the
family support of [exp-230](exp-230-h241-n12-additive-ceiling-3-9609.md), let the row
loop converge, and it converged below twelve, at $11.980$. That rejects the hypothesis as
registered: on this support the additive route is not dead at $3.9609$.

The converged value is a floating-point covering LP, not a certificate. Freezing it and
deciding it with the stock gate would test whether a point certificate proves
$s(12)\ge3.9609$, about $0.0009$ above T-017’s $3.96$, which X-047 estimated as n12’s
remaining additive headroom. That is a small increment of the kind the owner has asked to
deprioritize, recorded here as a cheap follow-up rather than selected.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
