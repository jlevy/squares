---
type: is
id: is-01m53czjmyrhwpdbvcwtx0ptka
title: "PR #644 review I: I3 self-contained retained-run fixture; I4 docstring line"
kind: task
status: in_progress
priority: 2
version: 2
delegate: user-eb
labels: []
dependencies: []
parent_id: is-01m51k8s0y2dbwnmvtwjv30zrx
hold: null
hold_until: null
created_at: 2026-10-16T22:23:05.373Z
updated_at: 2026-10-16T22:23:06.585Z
started_at: 2026-10-16T22:23:06.585Z
---
Review I on #644 (https://github.com/jlevy/squares/pull/644#pullrequestreview-5554317211). I3 (suggestion): test_a_decision_outranks_the_allowlist picks a live retained evand copy and would raise StopIteration if none remained; give it a tmp evidence= directory. I4 (nit): ragged docstring line at packing/devtools/default_drawings.py:93. Deferred so as not to restart #644's deep gate at its gated head; fix on the next branch touching default_drawings.py (e.g. #653 or the adoption PR).
