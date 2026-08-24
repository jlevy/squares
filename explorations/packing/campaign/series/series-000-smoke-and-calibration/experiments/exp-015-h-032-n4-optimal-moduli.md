---
title: exp-015 — H-032 exact n = 4 optimal moduli (in progress)
softschema:
  contract: packing.squares:Experiment/v1
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-015
  series: series-000
  title: H-032 exact n = 4 optimal moduli (in progress)
  date: '2026-08-24'
  hypotheses: [H-032]
  tier: confirmatory
  subject:
    label: full physical configuration space of four unit squares in side 2
    engine: exact small-n moduli checker 0.1.0
    engine_commit: d6bcff2
    precision: exact
    host_system: macOS arm64
    selftest_passed: false
  instance: {axis: n, point: 4, role: positive_control}
  method:
    control: n = 3 orientation-forcing lemma and the exact 2 x 2 grid
    candidate: exhaustive arbitrary-orientation classification and D4 x S4 orbit audit
    runs_per_condition: 1
    interleaved: false
    operator: openai-codex
    commit: d6bcff2
    dirty: false
    entry_point: explorations/packing/tools/check_small_n_moduli.py
    command: >-
      uv run --frozen python tools/check_small_n_moduli.py --n 4
      --record campaign/series/series-000-smoke-and-calibration/results/exp-015-h-032-n4-optimal-moduli.json
    budget: >-
      30 agent-minutes after exp-014; stop on one valid non-grid side-2 configuration,
      an orbit/stabilizer mismatch, or the replayed exact 24-state classification
    record: campaign/series/series-000-smoke-and-calibration/results/exp-015-h-032-n4-optimal-moduli.json
  lease:
    expires: '2026-08-24T13:30:00Z'
  results:
  - shape: determination
    question: in progress
    outcome: invalid
  verdict:
    decision: in-progress
    primary_criterion: exhaustive exact classification of F_4(2) and its S4 and D4 x S4 quotients
    reason: Claimed separately from n = 3; the common orientation lemma and exact orbit audit are being implemented.
---
# exp-015 — preregistered n = 4 rigidity corollary

This is a separate sweep cell even though it should be computationally free once the
orientation lemma is checked.
The round accepts the cell only if it proves that every side-2 packing is the
axis-aligned `2 x 2` grid, enumerates exactly 24 labelled configurations, and verifies
that both the `S4` quotient and the `D4 x S4` quotient are one point with the combined
stabilizer recorded.

A valid rotated or continuously moving side-2 configuration rejects the classification.
An incomplete orientation argument, state enumeration, group action, or exact replay
leaves it unresolved.
Nothing in this round is evidence about `n = 5` or `n = 6`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
