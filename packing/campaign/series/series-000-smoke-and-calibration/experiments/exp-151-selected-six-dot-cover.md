---
title: "exp-151 \u2014 selected wall tuple with six fixed dots"
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-151
  series: series-000
  title: Selected wall tuple with six fixed dots
  date: '2026-09-09'
  hypotheses:
  - H-149
  tier: exploratory
  subject:
    label: Fixed D plus the bound exp149 escape centre on wall tuple (0,0,0,7)
    engine: Existing exact polygon inclusion-exclusion with a fixed six-dot selected-wall adapter
    assurance: verified
    method: exact-algebraic
    host_system: Darwin arm64; project Python 3.14; one process
    selftest_passed: true
    engine_commit: c8cd38dad502c78840144bcae42df4294ba7f3d0
  instance:
    axis: n
    point: 11
    role: target
  method:
    control: Ten-obstacle subset ceiling, sixth-site escape rejection, source bindings and site ordering,
      first-deficit stop/replay and final-deadline controls; independent Astra Max source admission.
    candidate: Use the same four selected wall patches and D plus the exact exp149 centre. Check all 361
      directions with at most 1023 inclusion-exclusion subsets; stop at the first exact positive deficit
      with an independently replayed strict six-dot escape.
    runs_per_condition: 1
    interleaved: false
    operator: GPT-6 Astra coordinator; implementation by GPT-5.6 Sol extra high; mathematical admission
      by GPT-6 Astra max
    entry_point: packing/devtools/wall_owner_six_dot_cover.py
    command: cd packing && /opt/homebrew/bin/timeout --signal=TERM --kill-after=2s 300s .venv/bin/python3
      -m devtools.wall_owner_six_dot_cover campaign/series/series-000-smoke-and-calibration/results/agenda-032/exp-143-four-owner-footprint-cover.json
      campaign/series/series-000-smoke-and-calibration/results/agenda-033/exp-146-wall-owner-footprints.json
      campaign/series/series-000-smoke-and-calibration/results/agenda-033/exp-149-selected-wall-tuple-cover.json
      --expect-endpoint-blob cc66f06ddd3f7cc52d8a06d30a3920ba8e992c19 --expect-wall-blob e54fa98133db5f2135cae8875188f51b7db26e12
      --expect-wall-source 915758898a97c92793f51e62b7a6b17f846895ca --expect-selected-blob 83ec897738d6d1b228623c3ac4c10cd9170d5940
      --expect-selected-source 5600c0fb4eccf9e9dcdf82b02506d3d4340651cb --expect-git-revision "$(git rev-parse
      HEAD)" --deadline-seconds 240 --output campaign/series/series-000-smoke-and-calibration/results/agenda-033/exp-151-selected-six-dot-cover.json
    budget: One 300-second external process plus two-second grace and shared 240-second internal guard
      after input loading. No retry, tuning, replacement site, second tuple or inherited five-dot witness
      masks. Session121 phase3 latest launch is 18:25:55 UTC to fit before 18:30:57 UTC.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/agenda-033/exp-151-selected-six-dot-cover.json
    commit: c8cd38dad502c78840144bcae42df4294ba7f3d0
    dirty: false
  results:
  - shape: determination
    role: outcome
    question: Does fixed D plus the saved exp149 centre cover every required direction?
    outcome: criterion_missed
    checked_by: Directions 0 through 5 have exact zero deficit; direction 6 (owner-006) has positive exact
      deficit and an independently replayed rational escape avoiding all six sites and four selected patches.
  verdict:
    decision: rejected
    primary_criterion: Every one of the 361 required directions has exact zero uncovered area under the
      original transfer premises and six fixed distinct sites.
    reason: The completed first-deficit stop refutes this fixed six-dot set after seven of 361 directions.
      It does not rule out relocating the sixth site, changing other sites or a weighted certificate.
  effort:
    timebox: One 300-second external process plus two-second grace and shared 240-second internal guard;
      no retry.
    wall_seconds: 13.45
    stopped_by: criterion
---
# Exp151: The Fixed Sixth Dot Leaves Another Escape

**Rejected after one run.** The target launched at 18:22:02 UTC on 2026-09-09 from clean
published source `c8cd38dad502c78840144bcae42df4294ba7f3d0`, exited zero in 13.45
seconds, and produced a receipt byte-identical to captured stdout.
It checked seven directions: indices 0–5 have exact zero deficit, but owner-006 has a
positive deficit and a strict rational escape.
The independent replay includes all six sites and four patches.
Geometry measured 0.7116803329845425 seconds; the driver process measured
12.395755292003741 seconds.

This is a completed refutation, not a partial all-net traversal.
The first six directions show that the added site repaired the initial deficit, but not
the full family. H150/exp152 now separately tests whether any replacement sixth site
could hit both retained escapes.

## Frozen Prospective Protocol

Freeze the original five sites followed by the exact source-bound exp149 centre, tuple
`(0,0,0,7)`, four unchanged exp146 patches, and all 361 retained directions.
Publish admitted source and this protocol before the single run.

Accept only after all exact deficits are zero and the final deadline check passes.
Refute only at the first positive deficit accompanied by a rational core strictly inside
the container, avoiding all six closed dot conditions and all four selected patches.
Timeout before completed replay is partial; replay disagreement is invalid.
The augmented source must feed both area measurement and escape replay.

The
[design contract](../../../../cases/n11_five_dot_cover/after-exp150-decision-contract.md)
supplies the counting argument and controls.
Four owners leave seven residual cores; a six-dot cover would force two to share a dot.
This only excludes the selected owner tuple.
H146 remains a separate five-dot existence question, and no global bound or T023 grade
changes automatically.

If this fixed cover refutes, the
[conditional strategy](../../../../cases/n11_five_dot_cover/after-six-dot-refutation-strategy.md)
first tests whether any replacement sixth site can hit both saved escapes.
That screen has a separate prospective contract and is not run here.

The 240-second shared internal guard covers original saved-escape replay, six-dot
geometry, independent negative replay and the final decision.
Atomic publication is bounded by the 300-second external process plus two-second
termination grace. Preserve launch revision, clean state, UTC time, exit and timing.
No retry or second candidate.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
