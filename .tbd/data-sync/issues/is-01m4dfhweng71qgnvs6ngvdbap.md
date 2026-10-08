---
type: is
id: is-01m4dfhweng71qgnvs6ngvdbap
title: Investigate overview-fragment wall crossing in full integration
kind: task
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-10-06-exact-side-values.md
labels: []
dependencies: []
parent_id: is-01m4d2n7hjcxy6nh0wkvy8bpmj
created_at: 2026-10-08T10:04:44.884Z
updated_at: 2026-10-08T10:04:44.884Z
---
Full checkpoint37756689659 at a0ca63461 completed1799.15s gate/1968s run with11 passing deep/portability jobs, one main-gate failure plus dependent aggregate, and10 intentional skips. No functional assertions failed: fast behavioral shardC crossed its per-test wall ceiling because test_site_head.py::test_a_results_overview_is_a_fragment_with_no_head took12.43s against12s. Prior a910 checkpoint passed this test; mathematical data and renderer inputs are unchanged except small inline case-popover text and source metadata. Preserve fullattempt1; inspect source work path read-only and perform exactlyone failed-job retry on the same head with unchanged assertions/ceilings. Do not infer host cause from wall time or rerun until green. If repeated, retain a separate performance investigation with bounded profiling on adequate external storage. Evidence: validation/web-full-37756689659-a0ca6346-validate-failed.log and final run JSON.
