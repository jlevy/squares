---
type: is
id: is-01m5k93xejygzrdyf2k74g3wqe
title: Guard missing elements in retained browser probes
kind: task
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-10-22-site-navigation.md
delegate: root-navigation-final
labels: []
dependencies: []
parent_id: is-01m5k19kqedc9vp30sk9wm3s5f
hold: null
hold_until: null
created_at: 2026-10-23T02:23:24.112Z
updated_at: 2026-10-23T02:25:02.895Z
started_at: 2026-10-23T02:23:31.368Z
closed_at: 2026-10-23T02:25:02.894Z
close_reason: Published70102e8ea. Guarded DOM query reuse preserves probe behavior; fullbrowserfloor2steps passes32.25s includingalltypechecks and56liveness tests.
resolution: null
duplicate_of: null
---
Browser floor found two nullable-element arguments in case popover head and topic probe. Add explicit missing-element diagnostics, preserve checks, rerun browser floor.
