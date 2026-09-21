---
type: is
id: is-01m32sswmr56z2fg7atygb7yjx
title: Play grid-fill transitions at 3x, not 2x
kind: task
status: closed
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
created_at: 2026-09-21T20:16:32.407Z
updated_at: 2026-09-21T20:20:11.526Z
closed_at: 2026-09-21T20:20:11.525Z
close_reason: SIMPLE_TRANSITION_SPEED = 3; tests parameterised on the constant rather than its value.
resolution: null
duplicate_of: null
---
Owner's call: the simple transitions -- the ones where everything is square, the last rows of each grid fill -- should run at 3x rather than 2x.

`SIMPLE_TRANSITION_SPEED` in `packages/workbench/src/animation/timeline.ts` is currently 2. Raising it to 3 shortens every pair `isSpedUpPair` selects.

Note what must NOT change: `baseTiming` is deliberately free of the speed-up so physics steps are counted from the unsped span (fixed on main at 9afbb7e2a, where a 2x clock was simulating half the work for 159 grid fills). A Node test pins `pairTiming * speed == baseTiming`; it should keep passing at 3. `check_animation_editor` reads the `physics/steps-by-speed` probe and asserts the sped pair really plays faster, so the comparison stays non-vacuous.

Expect the corpus run to shorten: 159 simple pairs each losing a third rather than a half of their beat.
