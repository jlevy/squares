---
type: is
id: is-01m5a69fkfm8y1rgfx6dmyyprf
title: Guard empty current refinement roster in PR665 snapshot test
kind: task
status: in_progress
priority: 2
version: 2
delegate: codex-665-empty-roster-fix
labels: []
dependencies: []
parent_id: is-01m5a4zqkgk1vqa1q1n1ncbdec
hold: null
hold_until: null
created_at: 2026-10-19T13:40:50.926Z
updated_at: 2026-10-19T13:41:10.004Z
started_at: 2026-10-19T13:41:10.002Z
---
Own only packing/tests/test_refinement_custody.py: condition historical h.check_houses(ns) on nonempty ns, preserving unconditional c.check_index, custody copy/content/symlink assertions and snapshot cap. Preserve strict production empty-roster rejection. No heavy local work under W44 hold. Use before-red hosted failure and lightweight checks; normal-hook commit, exact-head guarded nonforce push to existing PR665 branch, focused honest body update. Root owns fresh review/changed-head hosted CI.
