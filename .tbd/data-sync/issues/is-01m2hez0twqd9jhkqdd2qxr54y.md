---
type: is
id: is-01m2hez0twqd9jhkqdd2qxr54y
title: "PR #160 review D89: stale references to deleted entry points"
kind: bug
status: closed
priority: 2
version: 5
labels: []
dependencies: []
parent_id: is-01m2hb40z4hvrre5f0219zp1m9
created_at: 2026-09-15T02:40:00.859Z
updated_at: 2026-09-15T03:54:47.892Z
closed_at: 2026-09-15T03:54:47.891Z
close_reason: "Fixed on #160: a3d6813f, 2cc60f7e, 6a316042, 9baad048, a093ec7a, and the annealing-plan line at b2588268."
resolution: null
duplicate_of: null
---
Review finding, PR #160 stack triage (2026-09-14), lane D-tools.

Stale references to deleted entry points: `grade_motion.py:208`; `build_candidate.py:1811`; the `check_candidate` docstring; annealing plan `:181` (`devtools/packing_strategy.py`); `capture_video.py:21` (`build_ascent`); eight spike instruments' default page; the package README's "local links".

Source: #160 R23 (non-spike-doc, non-benchmark items). Related: think-yz20, think-ekst, think-lmf5.

Files: the files named; `packages/workbench/README.md:43`; `docs/project/specs/active/plan-2026-09-11-annealing-as-a-search.md:181` (after lane B merges up).

## Notes

2026-09-14: fixed on #160 at a3d6813f (`grade_motion`, eight instrument defaults, package README), 6a316042 (`build_candidate.py` comments), 9baad048 (`check_candidate` docstring) and a093ec7a (`capture_video` docstring). Open: the annealing plan's `devtools/packing_strategy.py` line at `plan-2026-09-11-annealing-as-a-search.md:181`, which waits for lane B's merge-up.

2026-09-14: the annealing plan's executor line now names workbench_tools.strategy_execution (b2588268). Every D89 item is fixed.
