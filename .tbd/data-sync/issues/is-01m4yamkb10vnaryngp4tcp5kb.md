---
type: is
id: is-01m4yamkb10vnaryngp4tcp5kb
title: Resume task cleanup and CI measurements after scratch drive reconnects
kind: chore
status: in_progress
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4xkf4v65pthd9zbd7a5a3qv
hold: null
hold_until: null
created_at: 2026-10-14T23:05:56.308Z
updated_at: 2026-10-14T23:06:19.264Z
started_at: 2026-10-14T23:06:19.263Z
---
The external scratch volume /Volumes/spud-ext1 disappeared during CI stabilization. Builds, timing pairs and external cleanup are paused under the user scratch policy. Preserve active source, external environments, private historical profile and failed-test evidence. After reconnect: verify mount/writability, recheck exact candidate handles/owners, bind generated fixture directories to retained passing receipts, stage only disposable outputs using trash with a manifest, leave Trash unemptied, then resume the fresh main602 publication oracle and paired measurements. No internal fallback.
