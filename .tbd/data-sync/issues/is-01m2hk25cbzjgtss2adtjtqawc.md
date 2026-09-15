---
type: is
id: is-01m2hk25cbzjgtss2adtjtqawc
title: "PR #171 review D19: the simple-transition speed-up halves physics work"
kind: bug
status: closed
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m2hb41hy7fx18dy67asht84d
created_at: 2026-09-15T03:51:38.123Z
updated_at: 2026-09-15T03:53:16.784Z
closed_at: 2026-09-15T03:53:16.783Z
close_reason: "Fixed on PR #171 in 9afbb7e2: physics steps are priced from timeline.baseTiming, which the simple-transition speed-up does not shorten; pairTiming is what the clock plays. check_animation_editor's physics/steps-by-speed probe requires equal steps at 6 -> 7 and 4 -> 5 with the setting on and off (86 against 173 before), and a Node test pins pairTiming x speed = baseTiming."
resolution: null
duplicate_of: null
---
Canonical defect D19 from the 2026-09-14 stack triage (High). Source: #171 R3.

The simple-transition speed-up halves physics work in `api.physics` and the annealing benchmark. `physicsSteps` priced steps off `pairTiming`, which divides by `SIMPLE_TRANSITION_SPEED` for simple pairs while `fastSimple` is on (the default): at level 9, blind, physics style, the steps into 7, 8 and 14 ran 86 steps instead of 173.

Files: `packages/workbench/src/animation/timeline.ts:126-135`, `packages/workbench/src/application.js:1615-1622` @bb3f7c99, `packages/workbench/probes/bench-annealing.ts:250`.

Coordinator decision: keep the owner's 2x default (think-jk0f) and split displayed timing from physics steps, with a steps-invariance check. Feature bead: think-jk0f.
