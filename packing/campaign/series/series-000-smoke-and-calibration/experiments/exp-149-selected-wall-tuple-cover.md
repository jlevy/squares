---
title: exp-149 — exact cover of the selected small wall tuple
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-149
  series: series-000
  title: Exact cover of the selected small wall tuple
  date: '2026-09-09'
  hypotheses:
  - H-147
  tier: exploratory
  subject:
    label: Fixed five dots and wall tuple(0,0,0,7)
    engine: Independent exact polygon-union measurement with a thin source-bound selected-wall adapter
    assurance: verified
    method: exact-algebraic
    host_system: Darwin arm64; project Python 3.14; one process
    selftest_passed: true
    engine_commit: 5600c0fb4eccf9e9dcdf82b02506d3d4340651cb
  instance:
    axis: n
    point: 11
    role: target
  method:
    control: Source-bound thin-wrapper controls for the fixed tuple, complete coverage, first deficit
      and strict selected-patch escape, partial deadlines and malformed input/output; Astra Max source
      admission.
    candidate: Check the explicit tuple on the complete361 direction net. At the first positive deficit,
      extract one rational strict escape and independently replay it against the container, five dots
      and four selected wall footprints; stop.
    runs_per_condition: 1
    interleaved: false
    operator: GPT-6 Astra coordinator; implementation by GPT-5.6 Sol extra high; mathematical admission
      by GPT-6 Astra max
    entry_point: packing/devtools/wall_owner_selected_cover.py
    command: cd packing && /opt/homebrew/bin/timeout --signal=TERM --kill-after=2s 5m .venv/bin/python3
      -m devtools.wall_owner_selected_cover campaign/series/series-000-smoke-and-calibration/results/agenda-032/exp-143-four-owner-footprint-cover.json
      campaign/series/series-000-smoke-and-calibration/results/agenda-033/exp-146-wall-owner-footprints.json
      --expect-endpoint-blob cc66f06ddd3f7cc52d8a06d30a3920ba8e992c19 --expect-wall-blob e54fa98133db5f2135cae8875188f51b7db26e12
      --expect-wall-source 915758898a97c92793f51e62b7a6b17f846895ca --expect-git-revision "$(git rev-parse
      HEAD)" --deadline-seconds 240 --output campaign/series/series-000-smoke-and-calibration/results/agenda-033/exp-149-selected-wall-tuple-cover.json
    budget: One five-minute external process plus two-second grace and240-second cooperative internal
      guard after input loading. No tuning, retry, resume, seed bank or second tuple. Session118's latest
      launch16:18:07UTC and Session119's latest launch16:29:54UTC both expired unrun. The fresh unchanged
      Session120 latest launch is16:59:48UTC to fit before17:04:50UTC.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/agenda-033/exp-149-selected-wall-tuple-cover.json
    commit: 5600c0fb4eccf9e9dcdf82b02506d3d4340651cb
    dirty: false
  results:
  - shape: determination
    role: outcome
    question: Do the unchanged five dots cover the selected tuple at every required direction?
    outcome: criterion_missed
    checked_by: The complete source-bound receipt stopped at the first required direction, owner-000,
      with exact positive uncovered area71717500601808574131146882402353369/1245285277939023012815400000000000000.
      Its retained rational centre independently replays strict container, dot and selected-patch avoidance.
  verdict:
    decision: rejected
    primary_criterion: All361 unique required directions complete with exact zero uncovered area for tuple(0,0,0,7),
      with valid source bindings and physical transfer.
    reason: Direction owner-000 has a positive exact deficit and a validated rational strict escape,
      so the specified tuple fails the registered all361 zero-deficit criterion. This refutes H147 only;
      H146 remains unresolved over other tuples.
  effort:
    timebox: One five-minute external process with a240-second cooperative internal guard; one run,
      no retry or tuning.
    wall_seconds: 11.41
    stopped_by: criterion
---
# Exp149: The Selected Tuple Fails at the First Direction

**Rejected for the selected tuple.** The only target run launched at 16:40:34 UTC from
clean published revision `5600c0fb4eccf9e9dcdf82b02506d3d4340651cb` and exited zero
after 11.41 seconds.
Direction 0 (`owner-000`) has exact positive uncovered area
`71717500601808574131146882402353369/1245285277939023012815400000000000000`. The receipt
retains a rational centre that independently replays strict container, five-dot and
four-selected-patch avoidance.
It checked one of 361 directions because the registered negative criterion stops at the
first validated deficit; this is a complete refutation of H147, not a partial run.

The JSON is byte-identical to captured stdout.
It records 41 nonempty inclusion-exclusion subsets at the failing direction and binds
the unchanged endpoint and wall inputs to the published implementation.
H146 remains unresolved because it asks whether some other wall-owner tuple is covered
by the same dots.

**Prospective history, now discharged.** Sessions118 and119 expired without invocation.
Session120 carried the unchanged tuple, inputs, criteria and process allowance forward.
The tuple was fixed in the instrument, with no runtime selection mode.

Check all361 required unique directions using the selected exp146 footprints and the
unchanged exp143 five dots.
Accept only exact zero uncovered area everywhere with the retained physical transfer.
A first positive exact deficit must carry a rational core strictly inside the container,
avoiding every closed dot and all four selected closed owner patches; it refutes only
H147. A failure or timeout to produce required evidence is unresolved or invalid, never
a cover. H146’s broader existence question is not refuted by this candidate’s failure.

There is no nine-seed prerequisite and no complete WitnessBank is synthesized.
Exp148 remains partial.
Its
[analytic witness transport](../../../../cases/n11_five_dot_cover/after-exp148-strategy.md)
justifies why this tuple is tested next; the new cover checker needs only endpoint/D and
wall geometry bindings.
No new exp147/148 parser or 64-class escape broadcast is required.
A strict escape against the four selected patches suffices for this question.

All work after input loading shares the240-second cooperative guard; the external
five-minute ceiling includes loading and writing.
Preserve exact completed direction rows on cooperative partial return.
An external kill may leave no JSON; retain the process status and absence without
inferring a mathematical negative.

The
[source admission](../../../../cases/n11_five_dot_cover/selected-cover-source-admission.md)
separates exact finite coverage from the existing audited strict-core and owner
transfer. A new conditional exclusion would not itself exhaust n11 owner cases or change
the global bound.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
