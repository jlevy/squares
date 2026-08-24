---
title: exp-014 — H-032 exact n = 3 optimal moduli (in progress)
softschema:
  contract: packing.squares:Experiment/v1
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-014
  series: series-000
  title: H-032 exact n = 3 optimal moduli (in progress)
  date: '2026-08-24'
  hypotheses: [H-032]
  tier: confirmatory
  subject:
    label: full physical configuration space of three unit squares in side 2
    engine: exact small-n moduli checker 0.1.0
    engine_commit: d6bcff2
    precision: exact
    host_system: macOS arm64
    selftest_passed: false
  instance: {axis: n, point: 3, role: positive_control}
  method:
    control: Friedman central-point lemma plus the archived hard-square configuration-space literature
    candidate: exhaustive arbitrary-orientation classification and D4 x S3 orbit stratification
    runs_per_condition: 1
    interleaved: false
    operator: openai-codex
    commit: d6bcff2
    dirty: false
    entry_point: explorations/packing/tools/check_small_n_moduli.py
    command: >-
      uv run --frozen python tools/check_small_n_moduli.py --n 3
      --record campaign/series/series-000-smoke-and-calibration/results/exp-014-h-032-n3-optimal-moduli.json
      --svg atlas/n-003-optimal-moduli.svg
    budget: >-
      120 agent-minutes; stop on one valid genuinely rotated side-2 configuration, any
      mismatch in the labelled or quotient cell complexes, a source-premise failure,
      or a complete exact classification with deterministic record and SVG replay
    record: campaign/series/series-000-smoke-and-calibration/results/exp-014-h-032-n3-optimal-moduli.json
  lease:
    expires: '2026-08-24T13:30:00Z'
  results:
  - shape: determination
    question: in progress
    outcome: invalid
  verdict:
    decision: in-progress
    primary_criterion: exhaustive exact classification of F_3(2) and its S3 and D4 x S3 quotients
    reason: Claimed; the exact cell enumerator, orbit audit, source comparison, and deterministic renderer are being built.
---
# exp-014 — preregistered n = 3 configuration-space control

This round must classify the entire physical optimal set, not merely rediscover the
displayed sliding family.
Its first obligation is a checked equality argument excluding genuinely rotated side-2
packings.

Acceptance requires all of the following:

- a complete orientation-forcing proof in the open physical angle chart modulo each
  square’s quarter-turn redundancy;
- exact labelled counts of 24 vertices and 24 edges forming two circles;
- an exact `S3` quotient with four vertices and four edges forming one circle;
- an exact `D4 x S3` quotient homeomorphic to `[0, 1/2]`, with both endpoint stabilizers
  and the generic stabilizer recorded;
- the wall-incidence, contact-length, active-feature, and stabilizer transitions kept as
  distinct strata rather than collapsed into one endpoint hash;
- agreement with independently archived primary literature where that literature
  applies, with no novelty claim for the arbitrary-rotation or full-quotient
  refinements;
- exact rational packing samples accepted by the independent validity oracle, and the
  current geometric/contact keys agreeing with the declared strata;
- a deterministic SVG that shows the two labelled circles, the unlabelled circle, the
  quotient interval, and representative packing glyphs; and
- a separate replay that rejects deletion of one family, collapse of the two labelled
  components, a constant certificate on the closed family, and an injective use of the
  unreduced `t in [1/2,3/2]` display parameter.

One valid genuinely rotated packing rejects the proposed classification.
Any incomplete source recovery, cell enumeration, group action, stratum table, record
replay, or render replay leaves the round unresolved rather than partially accepted.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
