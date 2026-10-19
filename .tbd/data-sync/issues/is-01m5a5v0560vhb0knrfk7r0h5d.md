---
type: is
id: is-01m5a5v0560vhb0knrfk7r0h5d
title: Diagnose PR665 deferred slow CI timeout from retained evidence
kind: task
status: closed
priority: 2
version: 4
delegate: codex-665-slow-checkpoint-diagnosis
labels: []
dependencies: []
parent_id: is-01m5a4zqkgk1vqa1q1n1ncbdec
hold: null
hold_until: null
created_at: 2026-10-19T13:32:56.356Z
updated_at: 2026-10-19T13:39:09.682Z
started_at: 2026-10-19T13:33:06.818Z
closed_at: 2026-10-19T13:39:09.681Z
close_reason: "Bounded diagnosis delivered: confirmed empty-roster test defect; separate composite timing follow-up think-elpw remains open."
resolution: null
duplicate_of: null
---
Read-only remote CI forensic diagnosis for frozen PR665 3f20a458 against actual main 0ee05f4f3; no local tests/builds, no rerun/source edits/timeout increases/skips/publication. Inspect small deferred-slow timing journals from run 39256144591 and successful 39244113905/39239208628; identify unfinished node, phase/worker/count/order/timing and bind data-relevant source differences. Root owns next CI action.

## Notes

Read-only forensic diagnosis completed. No local tests/builds/stress/native/browser work, checkout materialization, source edits, CI reruns, timeout increases, skips or GitHub publication. Workflow: tbd shortcut review-code-performance narrowed by brief; tbd prime/policy show read. Effective main0ee05f4f3 policies workflows/editing/subagents granted, merge autonomous.

Evidence: https://github.com/jlevy/squares/actions/runs/39256144591/job/118072033267 ; raw log .codex/intake-resume-20261019/665-final-deferred-slow-failure.log . Artifact12189981845 validation-timings-deferred-slow-lane-1=34009bytes. Journal command097ff4e1d4374948a2ee9e40cc05f9b2, run_id cbdb7887727b46649dbe9e4470a5d325. Run metadata binds commitd4f629b0f52508513beed9a79a508396e14053cc, clean git_status/untracked{}, Python3.14.7, CPUs4, jobs1/inner_jobs2/PACK_JOBS2; actual pytest command uses -n4. GitHub git/commits confirms parents actualmain0ee05f4f3d0863f75c1036757839985e75655677 and frozen3f20a4584c50d95c02eab7c59193876afb0dd66a, treed478e0c89ca1e7048d4bf9f857fab931d6da9c64 equals local frozenhead tree. Command12:59:12.562048Z to13:29:13.564064Z wall1801.001206s, timed_out at1800s.

CONFIRMED FUNCTIONAL DEFECT: gw0 failure13:12:12.058938Z tests/test_refinement_custody.py::test_production_snapshot_copies_complete_refinement_custody, worker_order69, started13:11:48.221403Z/finished13:12:12.062861Z/23.841s. Full failure traceback retained in progress-gw0.jsonl: subprocess h.check_houses(ns) raises ValueError("unique refinement leaf roster required") at refinement_house_links.py125; assertion test_refinement_custody.py197. NUMBERS=(68,105,292) is unique and filter cannot add invalid/duplicate entries, so this rejection proves ns=[]. Main and both passing tested baselines: n68=[Rehwaldt n68 refinement2026-10-07], n105=[PingYou n105 refinement2026-10-12], n292=[Daniel regularized lists2026-10-10]; only68 matches historical refinement. PR665 moves68/105 to PingYou PR574 and292 stays Daniel, emptying roster. Strict production validator must retain empty-list rejection. Root will fix test fixture/empty-selection handling. Existing builder _retained_problems guards analogous call with if scoped.

OBSERVED COUNTS:227starts/226finishes=225passed+1failed. gw0=79finish/78pass1fail; gw1=19pass plus1active; gw2=93pass; gw3=35pass. Other workers session-finished by13:16:42.304145Z. gw1 active node tests/test_known_best_atlas.py::test_known_best_composite_contains_every_case_and_square, order20, started13:05:46.152963Z/setup passed13:05:46.153559Z; no call/finish through command end, call lowerbound1407.410s. Failed artifact has no JUnit XML. Stdout F obscured by aggregate timeout reporting: timeout-only diagnosis is incorrect.

BASELINES: https://github.com/jlevy/squares/actions/runs/39244113905 artifact12184390168 size64053bytes, tested27e87dac61878d2efc65b8ee798f78215eacee9a tree0b91c54592aa81115e5bf0f697e24bbd922f1b04; slow1534.437409s/241passed, composite gw1/order20 933.047s, refinement gw0/order69 24.699s pass. https://github.com/jlevy/squares/actions/runs/39239208628 artifact12182037784 size64350bytes, testedd51f88b7b79015a4ae785a59e2a015c257323757 treea90331f39b92ce035b5f45cc028de91b5b7a1488; slow1679.931461s/241passed, composite gw1/order20 1025.915s, refinement gw2/order48 27.975s pass. Same platform/Python/CPU/PACK_JOBS2/-n4 metadata; no host-resource telemetry proves variance.

SOURCE BINDING: gh api contents identities plus local git rev-parse show refinement testdc5a39c187ecaee383ec2be03d967c9db28a51c3 and validator59ae1d8198cfe0aff25a78d1e1209dd18de29b57 unchanged across main/bothpassing testedtrees/frozen665. Builder018a4476606d45b947f5b53d6646f5bcdad0432d unchanged throughout. Atlas test baseline/main5eae2210a4fbe37b4a7260ebe58309bd906ff3e8; frozen afc4fd159 changes unrelated poster assertions only, composite body unchanged. Active call expected_outputs->_built_corpus->built_cases->_build_case->_build_witness; adopted branch upper_bound_houses.build_witness->legacy.exact_verify.37 adopted witnesses/source routes changed. Example witness bytes n30896844->926274, n10577793->150721, n68251662->102157. Changed data may change work; no per-case/in-call telemetry localizes unfinished call. Neither hang nor measured growth cause established. Do not assert host variance.

COMMANDS: rg/sed/git diff/git cat-file/git rev-parse over read-only .worktrees/review-661-20261018; gh api metadata/contents/git-commits and small ZIP endpoints; packing/.venv/bin/python3 -B stdlib zipfile/json journal reads. External mount/writable verified via mkdir/test scoped escalation. TMPDIR,CARGO_TARGET_DIR,UV_CACHE_DIR explicitly external /Volumes/spud-ext1/agent-scratch/665-slow-checkpoint-diagnosis; pytest retention failed/count1 set. Small ZIPs retained there; only three slow journals used for conclusions. No whole large logs/bulk artifacts fetched.

HANDOFF: root fixes narrow test fixture, fresh Astra follow-up, hosted full rerun at changed head. Do not rerun frozen failing head.1800s cap preserved. Composite follow-up think-elpw remains OPEN under think-y03a; inspect corrected hosted timing and obtain bounded per-case/stack telemetry if still unresolved. Root owns next CI action.
