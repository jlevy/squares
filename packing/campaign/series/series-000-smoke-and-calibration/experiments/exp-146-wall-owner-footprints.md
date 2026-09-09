---
title: "exp-146 \u2014 all-sixteen wall-aware owner-footprint discriminator"
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-146
  series: series-000
  title: All-sixteen wall-aware owner-footprint discriminator
  date: '2026-09-09'
  hypotheses:
  - H-144
  tier: exploratory
  subject:
    label: Sixteen bottom-left owner classes with physical container-center constraints
    engine: Exact Fraction support extrema and convex intersections in devtools.wall_owner_footprints,
      using production owner_footprints geometry
    assurance: verified
    method: exact-algebraic
    host_system: Darwin arm64; project Python 3.14; one process
    selftest_passed: true
  instance:
    axis: n
    point: 11
    role: target
  method:
    control: Twelve synthetic tests, including exact point/segment public-wrapper clipping, distinct required
      frame rectangles, impossible versus partial disposition, signed provenance and diagonal reflection;
      Astra Max source admission.
    candidate: For every frozen owner class, intersect every common rectangle obtained from its nonempty
      physical center set; compare exactly with the old endpoint footprint.
    runs_per_condition: 1
    interleaved: false
    operator: GPT-6 Astra coordinator; implementation by GPT-5.6 Sol extra high; mathematical admission
      by GPT-6 Astra max
    entry_point: packing/devtools/wall_owner_footprints.py
    command: cd packing && /opt/homebrew/bin/timeout --signal=TERM --kill-after=2s 5m .venv/bin/python3
      -m devtools.wall_owner_footprints --expect-git-revision "$(git rev-parse HEAD)" --deadline-seconds
      240 --output campaign/series/series-000-smoke-and-calibration/results/agenda-033/exp-146-wall-owner-footprints.json
    budget: One five-minute external process with two-second termination grace and 240-second internal
      deadline. Complete sixteen classes in fixed order. No target tuning, retry, overwrite or resume.
      Launch no later than 08:33:50 UTC so the full guard and grace fit before 08:38:52. The original
      allocation expired unrun. Session116 forward-allocates the unchanged allowance; its latest launch
      is15:00:47UTC, fitting guard and grace before15:05:49UTC.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/agenda-033/exp-146-wall-owner-footprints.json
  results: []
  verdict:
    decision: in-progress
    primary_criterion: All sixteen classes complete validly with exact nesting for every feasible class,
      and at least one impossible class or one proper footprint inclusion.
    reason: The original Session115 allocation expired unrun during a network outage. User-authorized
      Session116 forward-allocates the unchanged single target after clean source publication; no target
      class evaluated yet.
  lease:
    expires: '2026-09-09T15:05:49Z'
    host: local
---
# Exp146: Test the Walls Across All Sixteen Classes

**Prospective and unrun.** The original Session115 allocation expired during the
user-confirmed network outage, with no invocation.
Session116 now forward-allocates the unchanged protocol after the user’s explicit
resumption request. Its target must launch by15:00:47UTC; the original cutoff below is
retained as history.

**Source admission.** Publish this protocol and the passing constructor before the one
target invocation. Capture the actual full launch commit, clean Git state, UTC start,
exit status and process duration.
The command resolves the published HEAD; it must match the separately captured launch
revision. Keep all launch metadata and stdout outside the repository until the driver’s
clean-tree check has passed.

Freeze q = 96/25, B = 9977/10000, both marks, all eight closed sectors, all 361
canonical directions and all 1444 signed rays.
For each retained frame, intersect its anchored quarter with the physical rectangle of
contained owner centers.
Preserve nonempty point and segment intersections.
Intersect the resulting support rectangles over every allowed frame; only a completed
all-empty frame list makes a class impossible.

Accept H144 only if the complete sixteen-class result contains at least one impossible
class or strict enlargement, with exact old-footprint nesting in every feasible class.
Reject only if all sixteen classes complete feasibly and all new footprints equal the
old ones. Failed controls, invalid provenance, geometry exceptions, guards and partial
manifests remain unresolved.
A proper inclusion is a geometry result, not an additional certified tuple.
BC318 will test whether it transfers either existing five-dot exclusion.

The source uses existing production geometry.
It is not an independent replay, does not optimize new dot weights, and cannot by itself
change T023 or the global n11 bound.
The [source admission](../../../../cases/n11_five_dot_cover/wall-source-admission.md)
and
[constructor contract](../../../../cases/n11_five_dot_cover/wall-constructor-contract.md)
state the mathematical premises.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
