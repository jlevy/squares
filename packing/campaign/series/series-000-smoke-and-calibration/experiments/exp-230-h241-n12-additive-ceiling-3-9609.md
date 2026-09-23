---
title: exp-230 — the additive ceiling at n12, side 39609/10000
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-230
  series: series-000
  title: The additive ceiling at n12, side 39609/10000
  date: '2026-09-23'
  hypotheses: [H-241]
  tier: confirmatory
  subject:
    label: >-
      Cutting loop at n=12, side 39609/10000, B = 9977/10000, 180 direction steps,
      seeded from T-017, in three legs (the second interrupted by an external SIGTERM
      and warm-restarted), with the depth-one family ceiling check after each iteration
    engine: >-
      devtools.run_fractional_cutting with colgen.check_ceiling at instrument commit
      69dac09a
    assurance: numerically-checked
    method: numerical-f64
    precision:
      binary_bits: 53
      rounding: nearest-even
    tolerance: A family counts only when the exact ceiling check proves total over maximum depth at least 12
    host_system: macOS, Claude Session 156 lane; project Python 3.14.7; single-process
  instance: {axis: n, point: 12, role: target}
  method:
    control: T-017's certificate at 99/25 as the seed; the ceiling readers' stock refusals
    candidate: >-
      Confirm H-241 on a proved ceiling with feasible total at least 12 accepted by
      both readers; reject when the loop settles below 12; an unsettled loop decides
      nothing.
    runs_per_condition: 1
    interleaved: false
    operator: Claude Session 156, Opus high lane
    entry_point: packing/devtools/run_fractional_cutting.py
    command: >-
      cd packing && uv run --frozen --all-extras --group dev python -m
      devtools.run_fractional_cutting --n 12 --side 39609/10000 --shrink 9977/10000
      --seed-certificate cases/n12_fractional_certificate/certificate.json, then two
      warm legs (exp-230-n12-run-leg2.command.txt, exp-230-n12-run-leg3.command.txt)
    budget: About 90 minutes of cutting plus the readers; three legs used about 2.5 hours.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/agenda-042/
  effort:
    timebox: About 90 minutes per leg
    wall_seconds: 9000
    stopped_by: timebox
  results:
  - shape: determination
    role: outcome
    question: >-
      Does the cutting loop prove a depth-one family of total over maximum depth at
      least 12 at side 39609/10000?
    outcome: no_progress
    checked_by: >-
      No leg proved a ceiling: the best scaled family totals were 10.704 (leg 1) and
      9.878 (leg 3), both failing K3 (total weight at least n), while the unconverged
      row objective stayed at 11.9796 to 11.9808 and was still rising; the loop never
      settled, so neither the confirm nor the reject condition was reached
  verdict:
    decision: unresolved
    primary_criterion: >-
      A proved ceiling of at least 12 confirms; a settled covering value below 12
      rejects; an unsettled loop decides nothing.
    reason: >-
      The loop ran to its time limits with the covering value unsettled just below 12
      and no family reaching 12, so whether additive routes at n12 survive above 3.9609
      is still open; a row objective of 11.98 is suggestive of a little headroom but is
      not a value.
    resume_from: >-
      The leg-3 warm state, retained as
      results/agenda-042/exp-230-n12-leg3-state.json.gz (about 17,500 sites and 10,356
      rows); exp-230-n12-run-leg3.command.txt names the settings to warm-start from it.
---
# Exp-230: The Additive Ceiling at n12, Side 39609/10000

[H-241](../../../hypotheses/H-241-n12-additive-route-dead-above-3-9609.md) was meant to
be a decisive negative: one ceiling run that closes every additive n12 route above
$3.9609$. It did not decide.
The best depth-one family the loop could prove reached about $10.7$ against the $12$ it
needed, while the row objective hovered at $11.98$, unconverged.
X-047 estimated n12’s additive headroom at about $0.001$ above T-017’s $3.96$; nothing
here contradicts that, and nothing confirms it.

A later attempt needs either a converged row loop, which means more rows per direction
and a longer clock than a shared host allowed tonight, or a family reader with a larger
support.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
