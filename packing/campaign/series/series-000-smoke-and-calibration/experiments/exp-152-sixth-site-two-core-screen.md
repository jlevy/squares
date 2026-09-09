---
title: "exp-152 \u2014 exact two-core screen for a replacement sixth site"
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-152
  series: series-000
  title: Exact two-core screen for a replacement sixth site
  date: '2026-09-09'
  hypotheses:
  - H-150
  tier: exploratory
  subject:
    label: Closed intersection of the two exact escaping B-cores from exp149 and exp151
    engine: Existing exact closed convex clipping with independent square SAT or vertex-membership replay
    assurance: verified
    method: exact-algebraic
    host_system: Darwin arm64; project Python 3.14; one process
    selftest_passed: true
  instance:
    axis: n
    point: 11
    role: target
  method:
    control: Target-blind disjoint, overlapping, edge-touching and point-touching square controls; source/pose/site
      provenance and deadline guards; independent mathematical source admission.
    candidate: Replay the two bound escaping cores, intersect their exact closed polygons, retain every
      dimension, and independently verify empty separation or common vertices. If nonempty choose only
      the mean of distinct vertices; no cover oracle runs here.
    runs_per_condition: 1
    interleaved: false
    operator: GPT-6 Astra coordinator; implementation by GPT-5.6 Sol extra high; mathematical admission
      by GPT-6 Astra max
    entry_point: packing/devtools/wall_owner_sixth_site_screen.py
    command: cd packing && /opt/homebrew/bin/timeout --signal=TERM --kill-after=2s 60s .venv/bin/python3
      -m devtools.wall_owner_sixth_site_screen campaign/series/series-000-smoke-and-calibration/results/agenda-032/exp-143-four-owner-footprint-cover.json
      campaign/series/series-000-smoke-and-calibration/results/agenda-033/exp-146-wall-owner-footprints.json
      campaign/series/series-000-smoke-and-calibration/results/agenda-033/exp-149-selected-wall-tuple-cover.json
      campaign/series/series-000-smoke-and-calibration/results/agenda-033/exp-151-selected-six-dot-cover.json
      --expect-six-dot-blob 46d34b1e295d9f5178379b02780a8c598c1a73e5 --expect-six-dot-source c8cd38dad502c78840144bcae42df4294ba7f3d0
      --expect-endpoint-blob cc66f06ddd3f7cc52d8a06d30a3920ba8e992c19 --expect-wall-blob e54fa98133db5f2135cae8875188f51b7db26e12
      --expect-wall-source 915758898a97c92793f51e62b7a6b17f846895ca --expect-selected-blob 83ec897738d6d1b228623c3ac4c10cd9170d5940
      --expect-selected-source 5600c0fb4eccf9e9dcdf82b02506d3d4340651cb --expect-git-revision "$(git rev-parse
      HEAD)" --deadline-seconds 30 --output campaign/series/series-000-smoke-and-calibration/results/agenda-033/exp-152-sixth-site-two-core-screen.json
    budget: One 60-second external process plus two-second grace and 30-second internal guard after inputs.
      No retry, third core, angle sweep or cover call. Phase4 latest launch18:53:07 UTC to fit before18:54:09
      UTC.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/agenda-033/exp-152-sixth-site-two-core-screen.json
  results: []
  verdict:
    decision: in-progress
    primary_criterion: The exact closed intersection is nonempty, with all retained vertices and the canonical
      candidate independently checked inside both cores.
    reason: Prospective and unrun; the fixed sixth site failed, but whether some replacement hits both
      escaping cores remains unknown.
  lease:
    expires: '2026-09-09T18:54:09Z'
    host: local
---
# Exp152: Screen Every Replacement Sixth Site Against Two Escapes

**Prospective and unrun.** Bind exp149 and exp151, replay both escapes against their
original D and D-plus-x149 domains, then intersect the two exact closed B-cores.
Use closed clipping that preserves points and segments.

Accept only a nonempty intersection with independently checked vertices and canonical
mean. Reject only empty intersection with an independent strict square separator.
Partial, invalid or missing source evidence is unresolved.
A nonempty screen is not an all-net cover; no new candidate is checked here.
An empty screen rules out the entire fixed-D-plus-one-site family, and also every
nonnegative added measure of mass below two while the five original unit atoms are
retained.

See the
[conditional proof and limits](../../../../cases/n11_five_dot_cover/after-six-dot-refutation-strategy.md).
Publish admitted source and this protocol before the one run; retain exact source
revision, clean state, UTC launch, exit, duration and receipt.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
