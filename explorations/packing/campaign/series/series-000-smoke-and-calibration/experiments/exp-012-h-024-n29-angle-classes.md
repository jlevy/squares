---
title: exp-012 — numerical n = 29 class count exposes H-024's formal-evidence gap
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-012
  series: series-000
  title: The numerical n = 29 reconstruction does not satisfy H-024's formal prerequisite
  date: '2026-08-24'
  hypotheses:
  - H-024
  tier: exploratory
  subject:
    label: high-precision reconstruction of the primary Kingbird n=29 SVG
    engine: kingbird SVG reconstruction checker 0.1.0
    engine_commit: '5384209'
    assurance: numerically-checked
    method: numerical-multiprecision
    precision:
      decimal_digits: 160
      rounding: nearest
    tolerance: 1e-80
    host_system: macOS arm64
    selftest_passed: true
  instance:
    axis: n
    point: 29
    role: target
  method:
    candidate: primary Kingbird square-29.svg witness
    runs_per_condition: 1
    interleaved: false
    operator: openai-codex
    commit: '5384209'
    dirty: true
    entry_point: explorations/packing/tools/check_kingbird_svg.py
    command: uv run --frozen python tools/check_kingbird_svg.py resources/papers/kingbird-square-29-provenance.svg
      --record campaign/series/series-000-smoke-and-calibration/results/exp-012-h-024-n29.json
    budget: 45 agent-minutes; one n=29 witness; stop on a failed numerical check or a numerical
      class count above 3
    record: campaign/series/series-000-smoke-and-calibration/results/exp-012-h-024-n29.json
  effort:
    timebox: 45m
    wall_seconds: 0.157556
    agent_minutes: 12
    stopped_by: criterion
  results:
  - shape: determination
    question: Does the retained n = 29 serialization numerically exhibit at most three orientation
      classes modulo quarter turns, and does it meet H-024's formal witness prerequisite?
    role: outcome
    outcome: criterion_missed
    checked_by: 'tools/check_kingbird_svg.py at 160 decimal digits: 29 unit squares, all 406 pairs
      checked, six non-overlapping angle intervals, and the SVG''s nine derived offsets plus six defining
      equations replayed below 1e-80'
  verdict:
    decision: unresolved
    primary_criterion: formally supported witness geometry with an orientation-class count at n = 29
    reason: The 160-digit numerical reconstruction has six well-separated classes, but the public
      serialization supplies no formal feasibility certificate, so it does not satisfy H-024's
      original prerequisite.
    commit: '5384209'
---
# exp-012 — six numerical classes leave H-024 formally unresolved

The predeclared numerical screen fired, but the registered claim required formally
supported record geometry.
The retained primary SVG reconstructs to 29 unit squares in side
`5.933833462676929189689460616352019…`. At 160 decimal digits and tolerance `1e-80`, all
406 pairs pass the numerical separating-axis guard, and the orientations form six
classes modulo quarter turns—not at most three.

| Class | Canonical angle | Squares |
| --- | ---: | ---: |
| aligned | `0°` | 15 |
| `a` | `25.2586553083514…°` | 1 |
| `b` | `20.8001267626996…°` | 9 |
| `−c` | `−17.5062684757324…°` | 1 |
| `d` | `24.9625879894377…°` | 2 |
| `i` | `24.3083584013469…°` | 1 |

The smallest gap between two declared classes is `a−d = 0.296067318913687…°`, against an
angle-interval radius of `1e-90°`. The numerical class count is therefore insensitive to
the declared clustering radius by roughly 89 orders of magnitude.

## Numerical check and source replay

[`exp-012-h-024-n29.json`](../results/exp-012-h-024-n29.json) is the raw record.
The checker expands four filled SVG polyominoes into 15 aligned squares, composes every
nested transform for the 14 rotated squares, checks unit shape and containment, and
tests every pair through the separate `sqpack.verify` SAT oracle.
Its mutation selftest duplicates one square and confirms that the oracle refuses it.

The worst nominal pair penetration is `4.05464e-101`, consistent with truncating the
source’s 200-digit numerical root to roughly 100 printed digits and far below the
declared `1e-80` serialization tolerance.
The smallest strictly positive pair separation is `0.0361709426628905`. As a second
guard, the checker independently recomputes all nine placement offsets and the six
equations printed in the SVG comment: maximum residuals are `1.11861e-99` and
`2.55681e-100`, respectively.

An independent read-only derivation reproduced the 15 aligned cells, the 14 transformed
square formulas, the class multiplicities, the SVG matrix order, and the `4.05464e-101`
worst nominal penetration before reading the checker output.

## What this decides

This round numerically contradicts the three-class pattern in the serialized source.
It does not formally refute H-024 because exact feasibility was a prerequisite of that
registered corpus claim.
[H-042](../../../hypotheses/H-042-n29-numerical-angle-classes.md) states the narrower
numerical claim and exp-037 reruns the check against it.
The observation also strengthens the reason to test H-025’s quantitative angle
compressibility instead of counting literal classes; it says nothing about H-001’s
algorithmic comparison.

The source calls the construction an exact analytic solution, but the retained SVG is a
high-precision `FindRoot` serialization, not an interval or symbolic certificate.
This round therefore establishes a numerically checked source reconstruction and a
six-class numerical count; it does not certify witness feasibility, the standing-record
value, or optimality.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
