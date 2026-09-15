---
type: is
id: is-01m2hk26bck710wdp1bnbcep6e
title: "PR #171 review D71: #171's checks and tests cannot fail on its defects"
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m2hb41hy7fx18dy67asht84d
created_at: 2026-09-15T03:51:39.115Z
updated_at: 2026-09-15T04:43:06.293Z
closed_at: 2026-09-15T04:43:06.293Z
close_reason: "Fixed on PR #171 in a0169823, d1930ea8 and 91cf28d6, with the checks in ac49b452 (lock sweep), 5bb067a0 (post-import stage), 9afbb7e2 (steps by speed) and 009ebb3c (separator side effects): the 159-step census, re-clamping in a 600 px window, the 1e-7/1e-4 degree tolerance edges and the removal of the constant assertion, each shown failing on a mutant."
resolution: null
duplicate_of: null
---
Canonical defect D71 from the 2026-09-14 stack triage (Medium). Source: #171 R7.

#171's new checks and tests cannot fail on its defects: the box beats are checked on one step where `to < open` (D18); the import runs after the box checks and never looks at the stage (D17); `simplePairs > 0` passes for any selection; the fixture assertion in `corpus.test.ts` reduces to "same side"; `assert.equal(SIMPLE_TRANSITION_SPEED, 2)` asserts a constant; `check_stage_resize` does not exercise re-clamping on resize or the keys' side effects (D69); nothing ties physics work to the speed-up (D19).

Files: `packages/workbench/tools/workbench_tools/check_animation_editor.py:78-85`, `:132-178`; `packages/workbench/tools/workbench_tools/check_stage_resize.py`; `packages/workbench/tests/corpus.test.ts:80-86`; `packages/workbench/tests/timeline.test.ts:72` @bb3f7c99.
