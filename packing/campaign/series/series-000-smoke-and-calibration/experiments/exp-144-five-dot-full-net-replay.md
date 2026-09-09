---
title: "exp-144 \u2014 exact full-net replay of the five-dot four-owner proposal"
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-144
  series: series-000
  title: Exact full361-direction replay of five four-owner dots
  date: '2026-09-09'
  hypotheses:
  - H-142
  tier: confirmatory
  subject:
    label: Published exp143 five equal-weight endpoint atoms and four-owner residual domain
    engine: devtools.replay_owner_footprint_cover using exact event-cell minima and reviewed vertical
      decomposition
    assurance: verified
    method: exact-algebraic
    host_system: Darwin arm64; project Python3.14.7; one process
    selftest_passed: true
    engine_commit: 5195c94c
  instance:
    axis: n
    point: 11
    role: target
  method:
    control: Bind clean tracked source Gitblobcc66f06ddd3f7cc52d8a06d30a3920ba8e992c19; reconstruct exact
      support, source directions, owner footprints, atoms and total mass.
    candidate: Replay unchanged endpoint atoms on all361canonical orientations. Every nonempty strict
      residual centre domain is checked exactly, with no symmetry reduction, LP, position change or reweighting.
    runs_per_condition: 1
    interleaved: false
    operator: GPT-6 Astra,max; session113 coordinator
    entry_point: packing/devtools/replay_owner_footprint_cover.py
    command: cd packing && /opt/homebrew/bin/timeout --signal=TERM --kill-after=2s 5m .venv/bin/python3
      -m devtools.replay_owner_footprint_cover campaign/series/series-000-smoke-and-calibration/results/agenda-032/exp-143-four-owner-footprint-cover.json
      --expect-receipt-blob cc66f06ddd3f7cc52d8a06d30a3920ba8e992c19 --scope full --max-atoms 1000 --max-event-cells
      5000000 --max-total-event-cells 10000000 --deadline-seconds 240 --output campaign/series/series-000-smoke-and-calibration/results/agenda-032/exp-144-four-owner-endpoint-full-net-replay.json
    budget: 'One five-minute external timeout plus two-second TERM grace;240second internal exact-loop
      deadline;1000atoms,5millioncells per direction and10milliontotal cells. Geometry-only preflight:
      five atoms,361nonempty directions,2457maximum cells and589549total. No target minimum inspected
      before registration.'
    record: packing/campaign/series/series-000-smoke-and-calibration/results/agenda-032/exp-144-four-owner-endpoint-full-net-replay.json
    commit: 5195c94c38c93f058894feb8679e49b0c4446823
  results:
  - shape: determination
    role: outcome
    question: Do the unchanged five dots cover every strict residual core on all361directions?
    outcome: criterion_met
    checked_by: Exact complete replay:361 unique directions, minimum1000001/1000000 at every direction;
      normalized total5. Source blobcc66f06ddd3f7cc52d8a06d30a3920ba8e992c19,589549densecells. Separate
      reviewed endpoint and strict-core transfer gives the conditional physical exclusion.
  verdict:
    decision: accepted
    primary_criterion: Complete all361directions and obtain exact minimum covered mass strictly greater
      than zero for the unchanged five equal-weight atoms.
    reason: All361directions have exact positive minimum beta=1000001/1000000. The five unit dots cover
      the residual net. Reviewed endpoint containment and strict-core transfer exclude the selected four-owner
      branch, which would need seven residual cores. No universal n11 exclusion.
  effort:
    timebox: Five-minute external guard and240second exact-loop guard
    wall_seconds: 28.95
    stopped_by: criterion
---
# Exp144: Exact Five-Dot Replay

**Completed:** all361directions passed at source5195c94c in28.95seconds. Every minimum
is beta; normalization gives exactly five unit dots.
The source path in the raw reader receipt is relative to the packing build directory;
its Gitblob and this record identify the repository-relative source unambiguously.
That display convention remains a small reader follow-up, not a changed input.

The numerical exp143 candidate has five atoms of common weight `beta = 1000001/1000000`.
Its total is `1000001/200000`. Every exact core mass is an integer multiple of beta.
Thus any positive complete minimum implies that the five unit dots cover the complete
residual net. A zero minimum rejects this specific proposal.
An incomplete reader is unresolved.

The reader certifies only the finite net.
The separately reviewed endpoint containment, full361orientation coverage, and
strict-core transfer establish the conditional physical implication.
No symmetry shortcut is available for these dots.
The four-owner part has a compatible physical realization; seven additional squares are
not asserted to fit.
One branch exclusion is not an exhaustive n11 theorem.

Commit and push source, reader, controls, and protocol before the one target run.
Preserve launch source, UTC, dirty state, exit, process time, and each direction’s exact
result. A reported zero should be turned into a geometric witness under a separate
diagnostic protocol, not silently retried with moved dots.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
