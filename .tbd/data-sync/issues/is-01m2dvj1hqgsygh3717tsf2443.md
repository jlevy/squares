---
type: is
id: is-01m2dvj1hqgsygh3717tsf2443
title: Bring the shared Pack step back to the old optimizer's cost
kind: task
status: open
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels:
  - workbench-roadmap
dependencies: []
parent_id: is-01m229an1fw0az9jgk0wcbg8c4
created_at: 2026-09-13T17:03:09.366Z
updated_at: 2026-09-15T04:55:11.492Z
---
Review 2026-09-13 benchmark: each live Pack step on the shared kernel (0f2ac8ce) costs 1.4-2.7x the retained optimizer's (n=17 1.7x, n=100 1.4x, sticky law 2.7x, n=307 2.1x, growth 2.0x). Causes: a full pose snapshot allocated every base step only to test finiteness (pack.ts ~711); receipt() measures geometry a second time and the app discards it (~543-548); updatePackRun clones and revalidates the whole configuration every frame including the N^2 mask twice (~495-505); growth recomputes inertia with an N^2 loop every substep (kernel.ts ~478-483). Playback at speed <= 2 does not show it; headless runs, Search and check_legend's n=307 runs do. Acceptance: think-tcns throughput benchmark before/after, parity fixture unchanged. Harness: scratch bench.ts from the review.

## Notes

2026-09-14, PR #160 review suggestion S2 ("Assess each frame once"), deferred here as part of Pack's per-frame cost; cheap. At `91cf28d6` (#171) each playing frame calls `PackController.state()` twice: `tick` reads `controller.state().configuration.physics.stepsPerSecond` (`src/app/pack-panel.ts:302`) and `redraw` calls it again (`:211`). `state()` (`src/app/pack-controller.ts:155-164`) exports the poses, runs `assessPackingSnapshot` and `structuredClone`s the result; the review measured 1.4 ms per call at n = 400. Read the configuration without cloning and assess once per frame, and measure before and after with think-tcns.
