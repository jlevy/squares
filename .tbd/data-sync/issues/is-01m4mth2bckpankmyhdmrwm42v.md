---
type: is
id: is-01m4mth2bckpankmyhdmrwm42v
title: "Reuse the reachable-tests probe's selection in the --run phase of the push tier (PR #496 review F5)"
kind: task
status: open
priority: 3
version: 1
spec_path: docs/project/specs/active/plan-2026-10-10-website-development-loop.md
labels:
  - packing
dependencies: []
parent_id: is-01m4ke1dkg5m43rszjm49ar77r
created_at: 2026-10-11T06:31:13.515Z
updated_at: 2026-10-11T06:31:13.515Z
---
From PR #496 review F, suggestion F5, deferred by the follow-up PR (think-jjs7).
`_push_test_step` runs `devtools.reachable_tests` twice (the `--summary` probe, then `--run`), and each repeats the import-graph scan: about 8 s each (selector 9.58 s minus 1.56 s of imports), both on the push critical path (`--push --list` 11.8 s vs `--edit --list` 1.6 s). The probe could write its selection (everything flag, reason, file list) into the snapshot directory the push path already creates, and `--run` read it instead of rescanning. Saves about 8 s per push (~5% of the 150 s cycle target) and guarantees both phases run identical file lists.
