---
title: exp-012 — H-024 at n = 29 (in progress)
softschema:
  contract: packing.squares:Experiment/v1
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-012
  series: series-000
  title: H-024 at n = 29 (in progress)
  date: '2026-08-24'
  hypotheses: [H-024]
  tier: exploratory
  subject:
    label: high-precision reconstruction of the primary Kingbird n=29 SVG
    engine: kingbird SVG reconstruction checker 0.1.0
    engine_commit: 6de2184
    precision: polished
    host_system: macOS arm64
    selftest_passed: false
  instance: {axis: n, point: 29, role: target}
  method:
    candidate: primary Kingbird square-29.svg witness
    runs_per_condition: 1
    interleaved: false
    operator: openai-codex
    commit: 6de2184
    dirty: false
    entry_point: explorations/packing/tools/check_kingbird_svg.py
    command: >-
      uv run --frozen python tools/check_kingbird_svg.py
      resources/papers/kingbird-square-29-provenance.svg
      --record campaign/series/series-000-smoke-and-calibration/results/exp-012-h-024-n29.json
    budget: 45 agent-minutes; one n=29 witness; stop on validity failure or a verified class count above 3
    record: campaign/series/series-000-smoke-and-calibration/results/exp-012-h-024-n29.json
  lease:
    expires: '2026-08-24T08:37:30Z'
  results:
  - shape: determination
    question: in progress
    outcome: invalid
  verdict:
    decision: in-progress
    primary_criterion: independently verified orientation-class count at n = 29
    reason: Claimed; the source reconstruction and independent validity check are running.
---
# exp-012 — one-witness falsifier for H-024

This round tests only the predeclared `n = 29` stop cell.
It does not infer a corpus-wide class count from a picture.
The witness must be reconstructed from the retained primary SVG, contain exactly 29 unit
squares, and pass an independent high-precision separating-axis check before its
orientation classes count.

The equality rule is fixed before the run: reduce every orientation modulo 90 degrees,
and merge two classes only when the SVG gives the same symbolic angle entity or when
their high-precision intervals overlap.
The five named nonzero entities `a`, `b`, `c`, `d`, and `i` are pairwise distinct in the
source decimals, so a valid reconstructed witness containing them plus the axis-aligned
class refutes the declared upper bound of three.

The round stops without a scientific verdict if the importer misses a square, the
validity guard fails, or the class identity is numerically ambiguous.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
