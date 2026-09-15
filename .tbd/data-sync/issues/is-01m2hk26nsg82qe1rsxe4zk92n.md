---
type: is
id: is-01m2hk26nsg82qe1rsxe4zk92n
title: "PR #171 review D91: the separator's aria-controls names the wrong pane"
kind: bug
status: closed
priority: 3
version: 2
labels: []
dependencies: []
parent_id: is-01m2hb41hy7fx18dy67asht84d
created_at: 2026-09-15T03:51:39.449Z
updated_at: 2026-09-15T04:16:20.615Z
closed_at: 2026-09-15T04:16:20.614Z
close_reason: "Fixed on PR #171 in 6ab61358: aria-controls names stage-wrap, and check_stage_resize requires the separator's value to be the height of the pane it names."
resolution: null
duplicate_of: null
---
Canonical defect D91 from the 2026-09-14 stack triage (Low). Source: #171 R8.

The separator's `aria-valuenow`, min and max are the stage's height, but `aria-controls="controls"`. The WAI-ARIA window-splitter pattern points `aria-controls` at the primary pane, the one the value measures: `stage-wrap`.

Files: `packages/workbench/assets/template.html:77` @bb3f7c99; `check_stage_resize.py` pins the wrong value. Feature bead: think-bau0.
