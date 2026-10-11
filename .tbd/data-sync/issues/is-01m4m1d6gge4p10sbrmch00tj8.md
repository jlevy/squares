---
type: is
id: is-01m4m1d6gge4p10sbrmch00tj8
title: Defer configuration-only push slow tests to the matching CI checkpoint
kind: task
status: closed
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-10-10-website-development-loop.md
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m4ke1dkg5m43rszjm49ar77r
hold: null
hold_until: null
created_at: 2026-10-10T23:12:12.303Z
updated_at: 2026-10-11T01:50:09.713Z
started_at: 2026-10-10T23:12:20.821Z
closed_at: 2026-10-11T01:50:09.712Z
close_reason: Implemented in merged6038af33. Independent admin verification confirms source,89 focused passes, clean floors, Astra reviews C/F and green final Packing38100510883 plus all ten Deferred38100526583 workers on identical merge tree61cd543d. No elapsed speedup claimed; prerequisite scoping remains think-9k61.
resolution: null
duplicate_of: null
---
Coordinator-authorized narrow execution placement policy: keep conservative reachable-test selection intact. Only nonempty change sets entirely within recognized suite configuration paths use all quick non-exhaustive tests locally; all mixed, unknown and source/record changes keep local slow tests. Existing required PR fast plus matching immutable-tree Deferred checkpoint provide complete slow/exhaustive coverage before merge. Preserve deadlines, budgets, pool complements, receipts and failure/empty-selection handling. Record focused execution and CI complement contract evidence; no overall wall savings claim. Prerequisite scoping remains the separate unimplemented think-9k61 follow-up.

## Notes

Frozen three-file implementation: packing/devtools/reachable_tests.py, packing/tests/test_reachable_tests.py and development.md. select_tests and every conservative fallback are unchanged. A nonempty path set entirely within SUITE_WIDE plus packing-validation.yml/deep-gate.yml uses the complete quick marker locally and reports the matching source/base PR-fast plus Deferred checkpoint requirement before merge. Any mixed renderer/scientific/test/record, unknown workflow, empty or unmapped change retains full non-exhaustive local execution. Pool normal/exclusive phases compose the same chosen marker; deadlines, budgets, failure/interrupt/empty-selection rules and existing command/progress/JUnit receipts are unchanged. Current renderer branch remains a mixed full fallback; this change does not shortcut its active broad run. Existing think-9k61 prerequisite-scoping work remains unimplemented.

Read-only coverage/cost rationale: both conftest.py and packing-validation.yml independently trigger full file selection even though their current changes only add the site timing mode and scoped frontend option. development.md already allows matching PR-fast plus Deferred checkpoint to cover the complete ordinary gate, and test_the_deep_gate_runs_exactly_what_the_pull_request_surface_defers checks the existing exact complement including slow and exhaustive lanes. Configuration-only local slow execution duplicated that checkpoint. The coordinator reports 65 prerequisites passed in 734 seconds on a saturated host and an active full behavioral run; these are retained context, not a measured speedup for this policy. No selector exemption, reduced CI coverage, deadline/budget increase or overall elapsed savings claim is part of this change.

Evidence: source external env, then PYTHONPATH=src:.:../packages/workbench/tools PYTEST_ADDOPTS= .venv/bin/python3 -m pytest -q tests/test_reachable_tests.py tests/test_validation_cli.py::test_push_tests_take_the_whole_suite_budget_only_when_the_selector_expands tests/test_deep_gate_workflow.py::test_the_deep_gate_runs_exactly_what_the_pull_request_surface_defers: 89 passed in 22.84 seconds. Existing execution cases cover mixed scientific/record/renderer and unknown paths, all quick roots, worker allocations and failure propagation; existing pool controls cover complementary markers, failures, interrupts and proved-empty lanes. Actual nested pytest proves quick tests run once and slow normal/pool tests defer only for configuration-only changes; directly selected slow tests still execute locally. JUnit: external tmp/config-only-push-policy-worktree.junit.xml. Initial receipt external tmp/config-only-push-policy.junit.xml retained: 88 passed and one Pages narrowing failure in 22.97 seconds because shared editable workbench_tools imported primary-checkout inputs outside managed REPO. Binding the worktree tools path corrected the environment; no guard or source selector was altered. Corrected focused command was already launched when coordinator requested only the failed case; no further run was launched.

Scoped BasedPyright on the two changed Python files: zero errors, warnings and notes. Scoped Ruff format/check, pinned flowmark-rs 0.4.0 auto/check on development.md and diff check passed. Source is frozen for Astra review. No commit, push, CI dispatch, broad build, PDF generation or unrelated job mutation performed. Keep child open until coordinator review and integrated publication/checkpoint evidence; parent think-ht59 remains open.
