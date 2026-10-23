---
type: is
id: is-01m5k2k8bj1rk2msdmp4qhdq73
title: Remove obsolete Recent Results daily and weekly renderer helpers
kind: task
status: in_progress
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-10-22-site-navigation.md
delegate: sol-deferred-notes
labels: []
dependencies: []
parent_id: is-01m5jnsqdwj3t8m7hkbx6mr1m2
hold: null
hold_until: null
created_at: 2026-10-23T00:29:26.768Z
updated_at: 2026-10-23T01:23:20.694Z
started_at: 2026-10-23T01:23:20.692Z
---
Senior review identified unused daily/weekly Recent Results renderer pipeline after replacement by one table. Remove only helpers/constants/styles proven exclusive and unused; preserve shared landed_day/added_reference and filtering utilities. Non-blocking cleanup follows the UI delivery; review actual consumers before removal.
