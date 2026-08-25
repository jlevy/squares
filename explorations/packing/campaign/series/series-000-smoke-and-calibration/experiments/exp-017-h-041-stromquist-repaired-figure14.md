---
title: exp-017 — one-coordinate repair certifies Stromquist's lower bound
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-017
  series: series-000
  title: Exact certificate for the repaired Stromquist five-node mechanism
  date: '2026-08-24'
  hypotheses:
  - H-041
  tier: confirmatory
  subject:
    label: source-distinct repaired Figure 14 point set at s = 2 + 4/sqrt(5)
    engine: Stromquist repaired-cover exact checker 0.1.0
    engine_commit: c6d036b
    assurance: verified
    method: exact-algebraic
    host_system: macOS arm64
    selftest_passed: true
  instance:
    axis: n
    point: 11
    role: calibration
  method:
    control: exp-016's exact printed-set escape, the printed G=.8 threshold failure, and source, tiling,
      boundary, sign, capacity, and duplicate-record mutations
    candidate: replace only G=(4/5,37/20) by G'=(79/100,37/20), then certify the complete Figure 13
      localization, A-triple forcing, repaired Figure 14 cover, and 3+9 count
    runs_per_condition: 1
    interleaved: false
    operator: openai-codex
    commit: c6d036b
    dirty: false
    entry_point: explorations/packing/tools/check_stromquist_repair.py
    command: uv run --frozen python tools/check_stromquist_repair.py --record campaign/series/series-000-smoke-and-calibration/results/exp-017-h-041-stromquist-repaired-figure14.json
      && uv run --frozen python tools/check_stromquist_repair.py --replay campaign/series/series-000-smoke-and-calibration/results/exp-017-h-041-stromquist-repaired-figure14.json
      > campaign/series/series-000-smoke-and-calibration/results/exp-017-h-041-stromquist-repaired-figure14-replay.json
    budget: 180 agent-minutes; stop on one uncovered center-space cell, one failed exact lemma premise
      or boundary, one source-scope mismatch, or a complete replayed five-node certificate
    record: campaign/series/series-000-smoke-and-calibration/results/exp-017-h-041-stromquist-repaired-figure14.json
  effort:
    timebox: 180m
    wall_seconds: 0.7
    agent_minutes: 90
    stopped_by: criterion
  results:
  - shape: determination
    question: Does moving only Figure 14 point G.x from .8 to .79 restore the complete lower-bound
      mechanism?
    role: outcome
    outcome: criterion_met
    checked_by: 'tools/check_stromquist_repair.py: exact source binding; complete Figure 13 and repaired
      Figure 14 cell complexes; exact lemma, root, sign, boundary, and capacity certificates; thirteen
      mutation controls; and deterministic complete-record replay'
  verdict:
    decision: accepted
    primary_criterion: every node of the source-distinct repaired five-node implication chain certifies
      exactly
    reason: The one-coordinate repair closes the unique failed outer cell while preserving a complete
      exact cover, so eleven freely oriented unit squares require side at least 2 + 4/sqrt(5).
    commit: c6d036b
---
# exp-017 — an exact repaired certificate for the `n = 11` lower bound

H-041 meets its preregistered criterion.
Replace only the printed Figure 14 point

`G = (4/5, 37/20)`

by the source-distinct point

`G' = (79/100, 37/20)`.

The exact checker then certifies every node of the lower-bound argument.

1. Eleven pairwise-disjoint open boxes and the ten Figure 13 points force one box to
   avoid all ten.
2. An exact 18-cell Figure 13 cover leaves only four exceptional rectangles in one
   Klein-four orbit.
3. Exact Lemma 4, Lemma 2, and Lemma 6 premises force that same box to contain all three
   points `A1`, `A2`, and `A3`.
4. The repaired Figure 14 center space is an exact 26-face tiling: thirteen outer lemma
   cells and thirteen central Lemma 2 triangles, with 28 vertices and 53 edges.
   Every vertex lies in the container, every internal edge has two incident faces, all
   boundary edges lie on the container, the complex is noncrossing, and its exact area
   is the container area.
5. The special box consumes at least three of the twelve capacity-one points, leaving
   ten other boxes for only nine points.

The repair closes precisely the cell that killed H-010. For the `G'`–`A1` quadrilateral,
Lemma 4 has `a=.95,b=.79`; its exact threshold lies above `.7981` and hence above `.79`.
The printed `.8` value remains an executable negative control.
Every edge in the thirteen-triangle central mesh remains shorter than one, and the
checker separately proves closure of shared edges and vertices under the strict open-box
semantics.

If eleven unit squares fit in a container of side smaller than `S = 2 + 4/sqrt(5)`,
uniform scaling into the side-`S` container turns them into eleven pairwise-disjoint
open squares of side strictly greater than one.
The certified five-node contradiction excludes that possibility.
Therefore this repository now has an exact, computer-assisted certificate that

`s(11) >= 2 + 4/sqrt(5)`.

This is a repair proposed and checked after exp-016; it is not Stromquist’s printed
point set and is not attributed to him.
The result has not undergone external peer review, and it does not close the gap to
Trump’s upper bound.

Generation and complete replay each took `0.35` wall seconds.
All thirteen mutations passed.
The retained result is
[`exp-017-h-041-stromquist-repaired-figure14.json`](../results/exp-017-h-041-stromquist-repaired-figure14.json).
The replay summary is
[`exp-017-h-041-stromquist-repaired-figure14-replay.json`](../results/exp-017-h-041-stromquist-repaired-figure14-replay.json).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
