---
title: exp-055 — H-059 n = 50 producer refusal ordering
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-055
  series: series-000
  title: Verify producer-bound existing-result refusal before every downstream seam
  date: '2026-09-01'
  hypotheses: [H-059]
  tier: exploratory
  subject:
    label: frozen n = 50 producer existing-result refusal ordering
    engine: sqpack n50 producer stage-sentinel harness 0.1.0-preregistered
    engine_commit: 81177148e404aa283c2a6ec7d696f2b39a9e361c
    assurance: verified
    method: exact-algebraic
    host_system: macOS arm64, Apple M1 Pro
    selftest_passed: false
  instance:
    axis: n
    point: 50
    role: calibration
  method:
    control: >-
      Independently calibrated bombs for binding observation, fixture loading, receipt
      evaluation and publication, plus reordered-stage, changed-runner, changed-result,
      overwrite and missing-sentinel mutations.
    candidate: >-
      The frozen producer dynamically loaded only after its digest is checked, with all
      four downstream seams replaced by live sentinels while the immutable exp-050
      result already exists.
    runs_per_condition: 1
    interleaved: false
    operator: openai-codex
    commit: 81177148e404aa283c2a6ec7d696f2b39a9e361c
    dirty: true
    entry_point: cases/n050_producer_refusal/run.py
    command: >-
      uv run --frozen python -m cases.n050_producer_refusal.run --record
      campaign/series/series-000-smoke-and-calibration/results/exp-055-h-059-n50-producer-refusal-ordering.json
    budget: >-
      BC-125 may perform at most 115 minutes of lane work through
      2026-09-02T02:10:00Z. It then stops until the common first-wave boundary at
      2026-09-02T02:45:00Z.
    record: campaign/series/series-000-smoke-and-calibration/results/exp-055-h-059-n50-producer-refusal-ordering.json
  lease:
    expires: '2026-09-02T02:45:00Z'
    host: local-macos-arm64
  results: []
  verdict:
    decision: in-progress
    needs_review: true
    primary_criterion: >-
      Both runtimes bind the frozen producer and result, emit the exact same refusal and
      canonical zero-call trace, leave exp-050 byte-identical and reject every named
      mutation after every sentinel proves live.
    reason: The prospective control is allocated and no producer observation has run.
---
# Exp-055 — H-059 `n = 50` Producer Refusal Ordering

The four sentinels must each fire once in a synthetic calibration before a zero-call
target trace can count.
The independent verifier imports neither this harness nor the frozen producer.

A pass validates only the prospective successor protocol.
It cannot alter exp-050, clear its review history, change H-054 or authorize source or
geometry work.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
