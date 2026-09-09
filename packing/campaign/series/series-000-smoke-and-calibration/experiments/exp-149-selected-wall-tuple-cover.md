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
  results: []
  verdict:
    decision: in-progress
    primary_criterion: All361 unique required directions complete with exact zero uncovered area for tuple(0,0,0,7),
      with valid source bindings and physical transfer.
    reason: Prospective and unrun. Analytic transport of retained exp148 witnesses selects this small
      explicit tuple before a general caching rewrite.
  lease:
    expires: '2026-09-09T17:04:50Z'
    host: local
---
# Exp149: One Explicit Small Tuple

**Prospective and unrun.** The Session118 and Session119 allocations expired without an
invocation. Session120 carries the unchanged tuple, inputs, criteria and process
allowance forward. Publish this allocation before the one target invocation.
Capture the exact full published revision, clean Git state, UTC start, process status
and elapsed time. Input blobs and constructor revision are fixed in the command.
The tuple is fixed in the instrument, with no runtime selection mode.

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
