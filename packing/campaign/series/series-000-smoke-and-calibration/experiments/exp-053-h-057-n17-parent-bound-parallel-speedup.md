---
title: exp-053 — H-057 n = 17 parent-bound parallel speedup
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-053
  series: series-000
  title: Profile parent-bound parallel execution on three fixed n = 17 directions
  date: '2026-09-01'
  hypotheses: [H-057]
  tier: exploratory
  subject:
    label: fixed-input parent-bound process speed and exact byte equivalence
    engine: sqpack n17 parent-bound parallel profiler 0.1.0-preregistered
    engine_commit: 81177148e404aa283c2a6ec7d696f2b39a9e361c
    assurance: verified
    method: exact-algebraic
    host_system: macOS arm64, Apple M1 Pro
    selftest_passed: false
  instance:
    axis: n
    point: 17
    role: calibration
  method:
    control: >-
      The unchanged exp-052 serial kernels on ordinals 33, 107 and 180, with the frozen
      checkpoint and progress inputs read-only.
    candidate: >-
      Three parent-bound worker processes writing disjoint fragments followed by one
      deterministic merger that validates and emits canonical rows.
    runs_per_condition: 3
    trials: 3
    interleaved: true
    operator: openai-codex
    commit: 81177148e404aa283c2a6ec7d696f2b39a9e361c
    dirty: true
    entry_point: benchmarks/n17_weighted_certificate_parallel.py
    command: >-
      From packing/, execute the four exact pair and assemble invocations in the Frozen
      Commands section once, in order; each pair has its own exclusive output root.
    budget: >-
      BC-123 receives 150 minutes through 2026-09-02T02:45:00Z. Measurement begins only
      after target-blind corruption controls and independent W2 admission pass.
    record: campaign/series/series-000-smoke-and-calibration/results/exp-053-h-057-n17-parent-bound-parallel-speedup.json
  lease:
    expires: '2026-09-02T02:45:00Z'
    host: local-macos-arm64
  results: []
  verdict:
    decision: in-progress
    needs_review: true
    primary_criterion: >-
      Median paired speedup is at least 2.8x, every candidate row and merged chain is
      byte-identical to serial, no pair is at or below 1x, and every corruption and
      interruption mutation rejects.
    reason: The round is allocated and no profile measurement has run.
---
# Exp-053 — H-057 `n = 17` Parent-Bound Parallel Speedup

This preregistration allocates the experiment and output paths before any writer or
profile starts. Exp-052 and its checkpoint and progress files remain read-only.

The three fixed ordinals are an admission discriminator.
They do not establish the cost of the remaining 148 directions or decide H-052.

## Frozen Commands

Run once from `packing/`, after W2 admission and with no competing CPU-heavy command:

```bash
uv run --frozen --all-extras --group dev python -m benchmarks.n17_weighted_certificate_parallel pair --experiment exp-053 --session session-073 --parent-checkpoint campaign/series/series-000-smoke-and-calibration/results/exp-052-h-052-n17-resumable-certificate-agreement.checkpoint.json --parent-progress campaign/series/series-000-smoke-and-calibration/results/exp-052-h-052-n17-resumable-certificate-agreement.progress.json --ordinals 33 107 180 --workers 3 --start-method spawn --pair-index 1 --order AB --output-root campaign/series/series-000-smoke-and-calibration/results/exp-053-h-057-n17-parent-bound-parallel-speedup.raw/pair-01-ab
uv run --frozen --all-extras --group dev python -m benchmarks.n17_weighted_certificate_parallel pair --experiment exp-053 --session session-073 --parent-checkpoint campaign/series/series-000-smoke-and-calibration/results/exp-052-h-052-n17-resumable-certificate-agreement.checkpoint.json --parent-progress campaign/series/series-000-smoke-and-calibration/results/exp-052-h-052-n17-resumable-certificate-agreement.progress.json --ordinals 33 107 180 --workers 3 --start-method spawn --pair-index 2 --order BA --output-root campaign/series/series-000-smoke-and-calibration/results/exp-053-h-057-n17-parent-bound-parallel-speedup.raw/pair-02-ba
uv run --frozen --all-extras --group dev python -m benchmarks.n17_weighted_certificate_parallel pair --experiment exp-053 --session session-073 --parent-checkpoint campaign/series/series-000-smoke-and-calibration/results/exp-052-h-052-n17-resumable-certificate-agreement.checkpoint.json --parent-progress campaign/series/series-000-smoke-and-calibration/results/exp-052-h-052-n17-resumable-certificate-agreement.progress.json --ordinals 33 107 180 --workers 3 --start-method spawn --pair-index 3 --order AB --output-root campaign/series/series-000-smoke-and-calibration/results/exp-053-h-057-n17-parent-bound-parallel-speedup.raw/pair-03-ab
uv run --frozen --all-extras --group dev python -m benchmarks.n17_weighted_certificate_parallel assemble --experiment exp-053 --session session-073 --raw-root campaign/series/series-000-smoke-and-calibration/results/exp-053-h-057-n17-parent-bound-parallel-speedup.raw --record campaign/series/series-000-smoke-and-calibration/results/exp-053-h-057-n17-parent-bound-parallel-speedup.json
```

The scored paired change is the median of `(parallel - serial) / serial`, not the ratio
of medians. The `2.8x` threshold is `change_pct <= -64.285714%`; every paired speedup
must also exceed `1x`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
