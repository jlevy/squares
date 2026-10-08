---
type: is
id: is-01m4de1sqb9njw6m6j9n0e3tp2
title: Recover PR435 workflow triggers from stale GitHub merge reference
kind: bug
status: in_progress
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-10-06-exact-side-values.md
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m4d2n7hjcxy6nh0wkvy8bpmj
hold: null
hold_until: null
created_at: 2026-10-08T09:38:29.226Z
updated_at: 2026-10-08T09:40:34.259Z
started_at: 2026-10-08T09:40:34.259Z
---
After native stack444 was linked, PR435 head advanced to a0ca63461 while refs/pull/435/merge remained c0ee1f82 with parents d948311d8 and old a910a0e6. Automatic Packing/Pages/Deferred checks were absent after both synchronize and a close/reopen refresh; push mergeability and exact-head full dispatch work. This matches the symptom reported in github/gh-stack issue319, without establishing the service cause. Recover the current merge reference through reversible stack metadata repair, preserve both branch heads and requested base, and require final PR-triggered plus full validation. Retain diagnostics outside disposable scratch.
