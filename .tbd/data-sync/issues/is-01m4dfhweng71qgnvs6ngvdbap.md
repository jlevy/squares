---
type: is
id: is-01m4dfhweng71qgnvs6ngvdbap
title: Investigate overview-fragment wall crossing in full integration
kind: task
status: in_progress
priority: 2
version: 5
spec_path: docs/project/specs/active/plan-2026-10-06-exact-side-values.md
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m4d2n7hjcxy6nh0wkvy8bpmj
child_order_hints:
  - is-01m4dj5bn5abmfwtszq9a2vzae
  - is-01m4dj5c1eanf3jhea0vfk9m3j
hold: null
hold_until: null
created_at: 2026-10-08T10:04:44.884Z
updated_at: 2026-10-08T10:50:20.589Z
started_at: 2026-10-08T10:07:01.510Z
---
Full checkpoint37756689659 at a0ca63461 completed1799.15s gate/1968s run with11 passing deep/portability jobs, one main-gate failure plus dependent aggregate, and10 intentional skips. No functional assertions failed: fast behavioral shardC crossed its per-test wall ceiling because test_site_head.py::test_a_results_overview_is_a_fragment_with_no_head took12.43s against12s. Prior a910 checkpoint passed this test; mathematical data and renderer inputs are unchanged except small inline case-popover text and source metadata. Preserve fullattempt1; inspect source work path read-only and perform exactlyone failed-job retry on the same head with unchanged assertions/ceilings. Do not infer host cause from wall time or rerun until green. If repeated, retain a separate performance investigation with bounded profiling on adequate external storage. Evidence: validation/web-full-37756689659-a0ca6346-validate-failed.log and final run JSON.

## Notes

Read-only source triage confirms no renderer/input-data work changed from a910a0e6 to a0ca6346. The changed case-popover script is outside this fragment path. test_site_head.py:508 calls render_overview.result_fragments()[0]; render_overview.py:1202 reloads the overview and eagerly renders every result despite the test inspecting only the first. It bypasses the documented shared render cache/module-fixture pattern in tests/site_renders.py:120. Reuse of the existing fixture is a plausible bounded improvement with original head assertions retained; not implemented in this slice and no source-level cause is established from one crossing. Earlier7.88s CPU lower bound and current12.43s call wall are not comparable measurements. Exactlyone failed-job rerun is attempt2 of37756689659 on identicala0ca6346; validator began2026-10-08T10:11:10Z. Preserve both attempts; this bead remains open for the source/cache improvement even if retry passes. No further local heavy tests because external free capacity was109MiB.
