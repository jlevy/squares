---
type: is
id: is-01m59eyytph14724m9yrwe5x3e
title: Prevent delayed profile requests from replacing newer native popovers
kind: bug
status: in_progress
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-10-10-contributor-profiles.md
delegate: profiles-popover-fix
labels: []
dependencies: []
parent_id: is-01m4v4ehd59t1r89qwksx77bmh
hold: null
hold_until: null
created_at: 2026-10-19T06:53:08.821Z
updated_at: 2026-10-19T06:53:15.646Z
started_at: 2026-10-19T06:53:15.644Z
---
Astra browser review reproduced: start delayed profile request from standalone credit, open ordinary native card/glossary popover, then release profile response. Old request replaces newer native panel. Unify cancellation/current-request ownership with native popover opens and add regression coverage.
