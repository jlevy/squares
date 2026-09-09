---
title: "exp-150 \u2014 saved-escape compatibility with selected owner cores"
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-150
  series: series-000
  title: Saved-escape compatibility with selected owner cores
  date: '2026-09-09'
  hypotheses:
  - H-148
  tier: exploratory
  subject:
    label: Exact exp149 escape versus the four selected snapped owner-core classes
    engine: Exact support extrema with independent square-polygon strict separation replay
    assurance: verified
    method: exact-algebraic
    host_system: Darwin arm64; project Python 3.14; one process
    selftest_passed: true
  instance:
    axis: n
    point: 11
    role: target
  method:
    control: Target-blind exact slack, strict tangency, complete class, provenance, corner transformation,
      independent pose replay and deadline controls; Astra Max source admission.
    candidate: For each fixed class in TR, BL, BR, TL order, minimize centre projection over each complete
      saved frame polygon and test the eight signed SAT axes. Stop at one fully incompatible class or
      four independently replayed compatible class witnesses.
    runs_per_condition: 1
    interleaved: false
    operator: GPT-6 Astra coordinator; implementation by GPT-5.6 Sol extra high; mathematical admission
      by GPT-6 Astra max
    entry_point: packing/devtools/wall_owner_escape_compatibility.py
    command: cd packing && /opt/homebrew/bin/timeout --signal=TERM --kill-after=2s 120s .venv/bin/python3
      -m devtools.wall_owner_escape_compatibility campaign/series/series-000-smoke-and-calibration/results/agenda-032/exp-143-four-owner-footprint-cover.json
      campaign/series/series-000-smoke-and-calibration/results/agenda-033/exp-146-wall-owner-footprints.json
      campaign/series/series-000-smoke-and-calibration/results/agenda-033/exp-149-selected-wall-tuple-cover.json
      --expect-endpoint-blob cc66f06ddd3f7cc52d8a06d30a3920ba8e992c19 --expect-wall-blob e54fa98133db5f2135cae8875188f51b7db26e12
      --expect-wall-source 915758898a97c92793f51e62b7a6b17f846895ca --expect-selected-blob 83ec897738d6d1b228623c3ac4c10cd9170d5940
      --expect-selected-source 5600c0fb4eccf9e9dcdf82b02506d3d4340651cb --expect-git-revision "$(git rev-parse
      HEAD)" --deadline-seconds 90 --output campaign/series/series-000-smoke-and-calibration/results/agenda-033/exp-150-wall-owner-escape-compatibility.json
    budget: One 120-second external process plus two-second grace and 90-second internal guard after inputs.
      No retry, additional pose, second tuple or tuning. Launch only with the full allowance remaining
      before 2026-09-09T19:06:40Z.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/agenda-033/exp-150-wall-owner-escape-compatibility.json
  results: []
  verdict:
    decision: in-progress
    primary_criterion: At least one selected class exhaustively has no strictly separated B-core across
      its complete retained frames and signed SAT axes.
    reason: Prospective and unrun; test the exp149 escape before changing dots or selecting another tuple.
  lease:
    expires: '2026-09-09T19:06:40Z'
    host: local
---
# Exp150: One Escape and Four Owner Classes

**Prospective and unrun; source admitted.** The saved exp149 escape and all geometry
sources are fixed by Git blobs.
Publish the admitted source and this protocol before the single target invocation.
Capture clean state, full published revision, UTC launch, process exit and elapsed time
automatically.

Acceptance requires an exhaustive class with maximum signed separation slack at most
zero. Strictly negative maximum also excludes a neighbourhood; zero excludes the exact
pose without establishing a positive-area improvement.
Refutation requires a verified compatible core for every selected class.
Stop after the first conclusively incompatible class or all four compatible classes.
Incomplete frame evidence, missing provenance, replay disagreement and deadlines never
establish a universal exclusion.

Use the
[reviewed model and quantifiers](../../../../cases/n11_five_dot_cover/after-exp149-strategy.md).
Neither an excluded pose nor four individually compatible cores settle a full residual
domain, unit-parent realizability, joint packing, H146 or a global n11 bound.

The 90-second internal guard covers saved-escape replay, geometry, independent class
replay and the complete decision before return.
JSON serialization, fsync and atomic publication fall under the 120-second external
process bound. An external kill can leave no JSON.

A conclusive result selects a separate future experiment: measure the stronger forbidden
region if a class excludes the escape; otherwise consider adding this centre as a sixth
dot on the same tuple.
No successor target is authorized by this protocol itself.
<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
