---
type: is
id: is-01m59eyytph14724m9yrwe5x3e
title: Prevent delayed profile requests from replacing newer native popovers
kind: bug
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-10-10-contributor-profiles.md
delegate: profiles-popover-fix
labels: []
dependencies: []
parent_id: is-01m4v4ehd59t1r89qwksx77bmh
hold: null
hold_until: null
created_at: 2026-10-19T06:53:08.821Z
updated_at: 2026-10-19T09:09:19.390Z
started_at: 2026-10-19T06:53:15.644Z
closed_at: 2026-10-19T09:09:19.390Z
close_reason: "Reviewed fixes integrated at b76a24fd29bdab28b5c946adeff88313fd28eb47. Standard packing and publication CI passed; full checkpoint passed with 14 successful jobs and 10 intentional skips: https://github.com/jlevy/squares/actions/runs/39223503977 . Final integration review: https://github.com/jlevy/squares/pull/578#pullrequestreview-5568927630 ."
resolution: null
duplicate_of: null
---
Astra browser review reproduced: start delayed profile request from standalone credit, open ordinary native card/glossary popover, then release profile response. Old request replaces newer native panel. Unify cancellation/current-request ownership with native popover opens and add regression coverage.
