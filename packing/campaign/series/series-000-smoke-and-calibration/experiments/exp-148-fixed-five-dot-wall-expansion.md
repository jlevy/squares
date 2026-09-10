---
title: exp-148 — fixed-five-dot witness bank and one candidate
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-148
  series: series-000
  title: Fixed-five-dot witness bank and one candidate
  date: '2026-09-09'
  hypotheses:
  - H-146
  tier: exploratory
  subject:
    label: Unchanged five dots on exp146 wall-owner residual domains
    engine: Exact dot-only vertical decomposition, independently replayed rational escape masks, and one
      full-net independent polygon-union check
    assurance: verified
    method: exact-algebraic
    host_system: Darwin arm64; project Python 3.14; one process
    selftest_passed: true
    engine_commit: 3bbb6987b5e752bcb0367e6b067707e941193454
  instance:
    axis: n
    point: 11
    role: target
  method:
    control: Exact component interior means, thin strips, strict dot/owner/container boundary refusal
      including an oblique rational frame, SAT replay of masks, product-union deduplication, known-certificate
      contradiction, deadlines and source-bound CLI output controls; Astra Max source review.
    candidate: Build the nine-direction dot-only witness bank and broadcast exact escape masks. If any
      nonbaseline tuple survives, select the lexicographically first and check at most that tuple across
      all361 directions; stop at the first deficit and independently replay and broadcast its escape.
    runs_per_condition: 1
    interleaved: false
    operator: GPT-6 Astra coordinator; implementation by GPT-5.6 Sol extra high; mathematical admission
      by GPT-6 Astra max
    entry_point: packing/devtools/wall_owner_fixed_pattern.py
    command: cd packing && /opt/homebrew/bin/timeout --signal=TERM --kill-after=2s 5m .venv/bin/python3
      -m devtools.wall_owner_fixed_pattern campaign/series/series-000-smoke-and-calibration/results/agenda-032/exp-143-four-owner-footprint-cover.json
      campaign/series/series-000-smoke-and-calibration/results/agenda-033/exp-146-wall-owner-footprints.json
      campaign/series/series-000-smoke-and-calibration/results/agenda-033/exp-147-wall-owner-containment.json
      --expect-endpoint-blob cc66f06ddd3f7cc52d8a06d30a3920ba8e992c19 --expect-wall-blob e54fa98133db5f2135cae8875188f51b7db26e12
      --expect-wall-source 915758898a97c92793f51e62b7a6b17f846895ca --expect-containment-blob 003befdf0b6db313658ad33eccb2b9af5fda61b0
      --expect-containment-revision e72102e15897dc33e59fcd82818a7ca9174d3cd0 --expect-git-revision "$(git
      rev-parse HEAD)" --deadline-seconds 240 --seed-deadline-seconds 60 --output campaign/series/series-000-smoke-and-calibration/results/agenda-033/exp-148-fixed-five-dot-wall-expansion.json
    budget: One five-minute external process plus two-second termination grace, a shared240-second internal
      clock and60-second seed-stage guard. No retry, tuning, resume or second candidate. Launch by16:05:07UTC
      to fit the full allowance before16:10:09UTC.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/agenda-033/exp-148-fixed-five-dot-wall-expansion.json
    commit: 3bbb6987b5e752bcb0367e6b067707e941193454
    dirty: false
  results:
  - shape: determination
    role: outcome
    question: Did a nonbaseline tuple complete the required all361 exact cover check?
    outcome: criterion_missed
    checked_by: Seed-stage cooperative deadline returned partial after two retained independently checked
      witnesses. Their product union rejects49152 labels, leaving16382 nonbaseline labels unclassified.
      No seed direction completed and no candidate was selected.
  verdict:
    decision: unresolved
    primary_criterion: At least one nonbaseline tuple completes all361 unique required directions with
      exact zero uncovered area and all input, witness and transfer guards valid.
    reason: The seed-stage guard expired before any complete seed direction or candidate check. Two valid
      retained escapes give reusable negative evidence for49152 labels, but neither a new cover nor an
      all-label refutation was completed.
    resume_from: Exp149 tests the separately registered explicit tuple(0,0,0,7) without extending or
      completing this partial seed bank.
  effort:
    timebox: One five-minute external process, shared240-second internal and60-second seed guards; no
      retry.
    wall_seconds: 74.03
    stopped_by: timebox
---
# Exp148: A Partial Witness Bank

**Unresolved.** The one run launched at 16:01:18 UTC from clean published
`3bbb6987b5e752bcb0367e6b067707e941193454` and returned exit 2 after 74.03 seconds.
The seed guard stopped the run after two useful axis-aligned witnesses, with zero
completed seed directions and no selected candidate.
Their exact product union rejects 49,152 class labels for this fixed pattern, leaving
16,382 nonbaseline labels.
The bank reports 66.18489845798467 seconds; the driver reports 73.42410541698337 seconds
including input loading.

The retained JSON is byte-identical to stdout.
It preserves the two rational centres, four masks per witness, input provenance and the
exact failure bitset.
The cooperative guard was checked after an exact operation crossed its deadline; the
external ceiling was respected.
This is useful partial evidence, not a completed nine-direction screen or a refutation
of the existence of an additional cover.

**Prospective history, now discharged.** Publish admitted source and this protocol
before one target. Capture its exact published revision, clean tree, UTC start, process
exit and elapsed seconds outside the repository.
Input blobs and upstream source revisions are fixed in the command.
Use a fresh output; never retry or overwrite the target.

The nine seed orientations carry folded indices 0,45,90,135,180, including reflected
sources, deduplicated geometrically and ordered by the full manifest.
At each seed, decompose the legal centre rectangle minus only the five closed dot-hit
polygons. Sample the exact mean of each positive-area component’s distinct vertices.
Independently check open container membership, strict dot avoidance and
square-versus-owner separation before broadcasting four sixteen-bit masks across the
tuple labels.

Deduplicate products rather than summing their sizes.
A checked witness must never refute an already certified baseline tuple.
One sample per dot-free component does not resolve every owner collision boundary, so
completing the seeds is not a full census.
The first surviving nonbaseline tuple is selected lexicographically in BL,BR,TL,TR
order, with m1:j0 through m1:j7 then m2:j0 through m2:j7 at each corner.

Check at most that one tuple across all361 required directions using its actual wall
footprints and the unchanged five dots.
Every completed direction retains its exact uncovered area and provenance.
At the first positive deficit, extract and independently replay a rational escaping
core, broadcast its masks, and stop candidate selection.
All stages share the total guard.
A dot lying inside a selected owner footprint is allowed; no outside-wall restriction is
added.

Accept only a new complete zero-deficit cover with all guards valid and the retained
physical transfer. Refute only if checked escapes cover every nonbaseline tuple.
Otherwise return unresolved, including when the selected candidate fails but other
labels remain. Removed-label counts are mechanism evidence; they do not replace the
existence criterion.
No escape proves a feasible packing of eleven unit squares.

Cooperative partial returns retain completed witnesses and directions in an atomic
receipt with typed failure status.
An external kill before the writer runs may leave no JSON; retain that absence and the
process status as incomplete evidence.
The five-minute external guard covers input loading and output, while internal clocks
cover their declared stages.
Do not infer refutation from a timeout.

The [strategy](../../../../cases/n11_five_dot_cover/after-wall-gain-strategy.md) and
[source admission](../../../../cases/n11_five_dot_cover/fixed-pattern-source-admission.md)
state the mathematical premises.
Additional conditional coverage does not automatically change T-023’s grade or the
global n11 bound.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
