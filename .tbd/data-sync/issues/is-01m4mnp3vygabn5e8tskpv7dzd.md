---
type: is
id: is-01m4mnp3vygabn5e8tskpv7dzd
title: "PR #496 G1: edit-tier Step.touches miss files the step's modules import"
kind: bug
status: closed
priority: 1
version: 4
delegate: claude-code@spud10
labels: []
dependencies: []
parent_id: is-01m4mneswbxt0m4w1caxy0x320
hold: null
hold_until: null
created_at: 2026-10-11T05:06:36.028Z
updated_at: 2026-10-12T23:39:01.973Z
started_at: 2026-10-11T05:06:53.418Z
closed_at: 2026-10-12T23:39:01.973Z
close_reason: "PR #496 review G1 fixed in PR #507 (merged 2026-10-12): attributed edit-tier steps claim their import closure, enforced by test_every_attributed_step_claims_the_modules_it_runs."
resolution: null
duplicate_of: null
---
High. packing/src/sqpack/cli/validate.py:4164-5300 (edit-tier Step.touches) with :7433-7435 (--push select_for_paths). 15 attributed edit-tier steps import files no touches pattern claims (23 with transitive gaps, 142 files); *.py is claimed by the lint floor, so no whole-gate fallback. Reproductions: [packing/src/sqpack/yamlio.py] drops retained JSON and published URL registry; [packing/devtools/audit_wand125_declared_net.py] drops FN1; [packing/devtools/__init__.py] drops three devtools-running steps. Fix (coordinator decision): add the missing claims and a contract test in tests/test_change_scoped_selection.py over the import graph (transitive if practical). Also correct the _CORE comment near :3994. PR #496, review G: https://github.com/jlevy/squares/pull/496#pullrequestreview-5481975880
