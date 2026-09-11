---
type: is
id: is-01m27jbzz13ja16var01e5r9wx
title: An intermediate tightening phase before the animation locks in to the record
kind: feature
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-09-09-packing-strategies-as-a-shared-language.md
labels: []
dependencies: []
created_at: 2026-09-11T06:27:07.359Z
updated_at: 2026-09-11T06:27:07.359Z
---
Under the physics style the run ends a visible distance from the record and the settle then snaps onto it, so the last thing a viewer sees is a jump rather than an arrival.

The owner asks for one more intermediate phase: tighten the physics result toward the record before the lock-in, so the final correction is small.

The Python side already has the mechanism this wants -- guide_home() in devtools/run_projection_ratchet.py drives a MOVING target rather than ramping a pull, which is what lands cleanly. The workbench needs the same beat: move (free physics), tighten (guided toward the record), settle (the remaining correction).

Measure first: how far off is the physics result at moveEnd, per n? That number decides whether the tighten phase needs to be long or whether the snap was just badly placed.
