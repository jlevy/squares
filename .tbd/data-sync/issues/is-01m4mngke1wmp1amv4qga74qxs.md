---
type: is
id: is-01m4mngke1wmp1amv4qga74qxs
title: "Reuse the --push probe's reachable-test selection in the --run phase (PR #496 F5)"
kind: task
status: closed
priority: 3
version: 2
spec_path: docs/project/specs/active/plan-2026-10-10-website-development-loop.md
labels: []
dependencies: []
parent_id: is-01m4ke1dkg5m43rszjm49ar77r
created_at: 2026-10-11T05:03:35.359Z
updated_at: 2026-10-12T23:39:10.734Z
closed_at: 2026-10-12T23:39:10.734Z
close_reason: "Duplicate of think-tqwo (PR #496 review F5), which PR #507 and the website development-loop plan name as the owner."
resolution: duplicate
duplicate_of: is-01m4mth2bckpankmyhdmrwm42v
---
Deferred from PR #496 review F, suggestion F5 (pre-existing): https://github.com/jlevy/squares/pull/496#pullrequestreview-5481911429
_push_test_step (packing/src/sqpack/cli/validate.py:5832 probe, :5859 --run) runs devtools.reachable_tests twice and each run repeats the import-graph scan: about 8 s per run (selector 9.58 s minus 1.56 s of imports). Both are on the push critical path (--push --list 11.8 s vs --edit --list 1.6 s). The probe could write its selection (everything flag, reason, file list) into the snapshot directory PR #496 already creates, and --run could read it: about 8 s saved per push, and both phases then run identical file lists.
Waits on: a selection-file contract between the probe and --run (schema, fail-closed reading), designed with the think-ht59 development-loop work.
