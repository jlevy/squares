---
title: exp-014 — exact n = 3 optimal moduli form a quotient interval
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-014
  series: series-000
  title: Exact classification of the full n = 3 optimal configuration space
  date: '2026-08-24'
  hypotheses:
  - H-032
  tier: confirmatory
  subject:
    label: full physical configuration space of three unit squares in side 2
    engine: exact small-n moduli checker 0.1.0
    engine_commit: 257cb0d
    assurance: verified
    method: exact-algebraic
    host_system: macOS arm64
    selftest_passed: true
  instance:
    axis: n
    point: 3
    role: positive_control
  method:
    control: Friedman central-point lemma plus the archived hard-square configuration-space literature
    candidate: exhaustive arbitrary-orientation classification and D4 x S3 orbit stratification
    runs_per_condition: 1
    interleaved: false
    operator: openai-codex
    commit: 257cb0d
    dirty: false
    entry_point: explorations/packing/tools/check_small_n_moduli.py
    command: uv run --frozen python tools/check_small_n_moduli.py --n 3 --record campaign/series/series-000-smoke-and-calibration/results/exp-014-h-032-n3-optimal-moduli.json
      --svg atlas/n-003-optimal-moduli.svg && uv run --frozen python tools/check_small_n_moduli.py
      --n 3 --replay campaign/series/series-000-smoke-and-calibration/results/exp-014-h-032-n3-optimal-moduli.json
      --check-svg atlas/n-003-optimal-moduli.svg
    budget: 120 agent-minutes; stop on one valid genuinely rotated side-2 configuration, any mismatch
      in the labelled or quotient cell complexes, a source-premise failure, or a complete exact classification
      with deterministic record and SVG replay
    record: campaign/series/series-000-smoke-and-calibration/results/exp-014-h-032-n3-optimal-moduli.json
  effort:
    timebox: 120m
    wall_seconds: 0.63
    agent_minutes: 30
    stopped_by: criterion
  results:
  - shape: determination
    question: What is the full physical side-2 configuration space at n = 3 and its S3 and D4 x S3
      quotients?
    role: outcome
    outcome: criterion_met
    checked_by: 'tools/check_small_n_moduli.py: exact orientation forcing, 64 separation disjuncts,
      24 consistent one-cells, independent exact packing samples, complete quotient/stabilizer tables,
      scoped literature comparisons, nine mutation controls, and byte-identical semantic and SVG replay'
  verdict:
    decision: accepted
    primary_criterion: exhaustive exact classification of F_3(2) and its S3 and D4 x S3 quotients
    reason: F_3(2) is two labelled 12-cycles; its S3 quotient is one four-cycle and its D4 x S3 quotient
      is the interval [0,1/2], with every physical configuration axis-aligned and all three quotient
      strata replayed exactly.
    commit: 257cb0d
---
# exp-014 — the complete optimal moduli space at n = 3

The preregistered control passed.
It classifies the entire physical optimal set, not merely the displayed sliding family.

## Orientation forcing

Center the side-2 container at the origin and let `w = |cos(theta)| + |sin(theta)|` for
one unit square.
Its axis-aligned half-extent is `w/2`, so containment bounds each center
coordinate by `1 - w/2`. Projection onto either local square axis is therefore at most

`w(1 - w/2) = 1/2 - (w - 1)^2/2`.

The container center lies in every contained unit square and lies in the interior of
every genuinely rotated one.
With a second square present, that interior contains points from the second square’s
interior, contradicting disjoint interiors.
Thus every side-2 packing here is axis-aligned.

## Exact cell and quotient classification

Axis-aligned lower-left coordinates lie in `[0,1]^2`. For each of the three square
pairs, nonoverlap is the four-way disjunction left, right, below, or above.
Of 64 raw choices, exactly 24 are consistent; every consistent cell has one free
coordinate. Their endpoints are 24 labelled corner states and their 24 edges form two
disjoint 12-cycles, so the labelled Betti vector is `[2,2]`.

Relabelling identifies the two cycles and reduces the complex to the four-cycle of the
missing grid corner, with Betti vector `[1,1]`. The `D4` action is transitive on its
four vertices and four edges.
After subdividing at reflection-fixed edge midpoints, the full `D4 x S3` quotient is the
closed interval `lambda in [0,1/2]`.

Its three orbit strata are:

- `C`, the corner/L endpoint: dimension zero, local dimension one, stabilizer two, six
  wall incidences, three pair contacts, and four active SAT axes;
- `G`, the open generic stratum: dimension and local dimension one, trivial stabilizer,
  five wall incidences, three pair contacts, and three active axes; and
- `M`, the centered endpoint: dimension zero, local dimension one, stabilizer two, with
  the same active signature as `G`.

This separates an active-contact change at `C` from a pure stabilizer jump at `M`. It
also fixes D-140: the closed displayed family has two current contact certificates, not
one. The open stratum and `M` share one certificate; `C` has the second, while all three
remain in the same connected family.

## Independent checks, sources, and cost

Exact rational representatives pass the independent packing oracle.
Four quotient samples have distinct geometric keys; the three non-corner samples share
one contact certificate and the corner sample differs.
The labelled counts agree with Alpert et al.
(2023), and the unlabelled circle agrees with the applicable homotopy statement of
Alvarado-Garduño and González (2025). The result names the retained source paths and
keeps their scopes separate.
Plakhta (2021) remains unavailable, so this round makes no novelty claim.

Generation took 0.32 wall seconds and a separate full rebuild plus byte comparison took
0.31 seconds. All nine known-answer mutations passed.
The deterministic map is
[`n-003-optimal-moduli.svg`](../../../../atlas/n-003-optimal-moduli.svg).
The retained result is
[`exp-014-h-032-n3-optimal-moduli.json`](../results/exp-014-h-032-n3-optimal-moduli.json).

This answers only the `n = 3` cell of H-032. It does not classify larger containers or
`n >= 5`.

## Preregistered acceptance rule

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
Any incomplete recovery of a source used as corroboration, cell enumeration, group
action, stratum table, record replay, or render replay leaves the round unresolved
rather than partially accepted.
The unavailable Plakhta paper blocks novelty claims, not this independent
classification, and remains tracked separately.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
