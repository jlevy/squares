---
type: is
id: is-01m4m6yg8cnpm1pz0jsg77jv2n
title: Diagnose initial-fragment Headroom startup race
kind: task
status: in_progress
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m4m588mffw9ac4ssy5qa9hhd
hold: null
hold_until: null
created_at: 2026-10-11T00:49:02.219Z
updated_at: 2026-10-11T00:49:35.834Z
started_at: 2026-10-11T00:49:35.832Z
---
Own test_site_headroom.py and dedicated probes. Diagnose hosted failure where initial fragment navigation leaves header hidden; repair only a stale or timing-sensitive oracle, otherwise report product defect to root for shared-source fix. Run focused browser case and the Headroom module. No commit or push.
