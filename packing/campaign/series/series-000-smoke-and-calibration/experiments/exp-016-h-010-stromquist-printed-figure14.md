---
title: exp-016 — Stromquist's printed Figure 14 set is avoidable
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-016
  series: series-000
  title: Exact refutation of the printed Figure 14 unavoidability claim
  date: '2026-08-24'
  hypotheses:
  - H-010
  tier: confirmatory
  subject:
    label: Stromquist's printed twelve-point Figure 14 set at s = 2 + 4/sqrt(5)
    engine: Stromquist Theorem 2 exact checker 0.1.0
    engine_commit: 178fc6b
    assurance: verified
    method: exact-algebraic
    host_system: macOS arm64
    selftest_passed: true
  instance:
    axis: n
    point: 11
    role: calibration
  method:
    control: source-bound printed tuples, strict open-box semantics, and capacity mutations
    candidate: exact algebraic strict box avoiding all twelve printed Figure 14 points
    runs_per_condition: 1
    interleaved: false
    operator: openai-codex
    commit: 178fc6b
    dirty: false
    entry_point: explorations/packing/tools/check_stromquist_theorem2.py
    command: uv run --frozen python tools/check_stromquist_theorem2.py --record campaign/series/series-000-smoke-and-calibration/results/exp-016-h-010-stromquist-printed-figure14.json
      && uv run --frozen python tools/check_stromquist_theorem2.py --replay campaign/series/series-000-smoke-and-calibration/results/exp-016-h-010-stromquist-printed-figure14.json
      > campaign/series/series-000-smoke-and-calibration/results/exp-016-h-010-stromquist-printed-figure14-replay.json
    budget: 240 agent-minutes for source reconstruction, exact witness certification, and adversarial
      replay; stop on one strict certified escape, a complete five-node reproduction, or any unresolved
      source or exact-field boundary
    record: campaign/series/series-000-smoke-and-calibration/results/exp-016-h-010-stromquist-printed-figure14.json
  effort:
    timebox: 240m
    wall_seconds: 0.55
    agent_minutes: 180
    stopped_by: criterion
  results:
  - shape: determination
    question: Does Stromquist's printed five-node Theorem 2 mechanism reproduce exactly?
    role: outcome
    outcome: criterion_missed
    checked_by: 'tools/check_stromquist_theorem2.py: retained source paths and exact point tuples,
      a strict algebraic Figure 14 escape, independent containment and avoidance expressions, corrected
      Lemma 4 root filtering, ten mutation controls, and deterministic complete-record replay'
  verdict:
    decision: rejected
    primary_criterion: all five source-faithful implications reproduce under exact replay
    reason: The printed Figure 14 set is avoidable, so node four and therefore the five-node conjunction
      fail; this rejects the proof as printed, not the numerical lower bound.
    commit: 178fc6b
---
# exp-016 — an exact escape from the printed Figure 14 set

H-010 is rejected on its original, source-faithful claim.
The checker certifies an open square of side

`L = 10001/10000`

with `tan(theta) = 27/10` and centre `(37L/(2 sqrt(829)), 11/8)`. It lies inside
Stromquist’s container of side `2 + 4/sqrt(5)` and strictly avoids every one of the
twelve points printed in Figure 14. The smallest exact avoidance margin occurs at
`G = (4/5, 37/20)` and is approximately `4.93957e-5`; the next is at `A1`.

The witness pinpoints the same outer quadrilateral that the source routes through Lemma
4\. In its local coordinates, that cell has parameters `a = .95`, `b = .8`, while the
true threshold is about `.7981534378`. The paper’s squared stationary cubic also
contains an extraneous root in a different table row; the checker filters every
candidate through the unsquared sign condition.

The source boundary matters.
The exact record binds the retained 2003 PDF and raw extraction, reconstructs the Figure
13 point set under its actual Klein-four symmetry, and rejects a false `D4` expansion.
It also checks the conditional `3 + 9` capacity argument and demonstrates why standalone
twelve-point unavoidability would not by itself exclude eleven boxes.
The Figure 13 escape in the record is constructive evidence, not a universal
localization certificate; node four already refutes the registered conjunction.

Generation took `0.33` wall seconds and complete deterministic replay took `0.22`
seconds. All ten mutations passed.
The retained result is
[`exp-016-h-010-stromquist-printed-figure14.json`](../results/exp-016-h-010-stromquist-printed-figure14.json).
The replay summary is
[`exp-016-h-010-stromquist-printed-figure14-replay.json`](../results/exp-016-h-010-stromquist-printed-figure14-replay.json).

This result invalidates Stromquist’s published proof as printed.
It does **not** refute the lower bound `s(11) >= 2 + 4/sqrt(5)`: a nearby point-set
repair may establish the same inequality by a source-distinct argument.
That separately preregistered test is H-041.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
