---
type: is
id: is-01m4yamkb10vnaryngp4tcp5kb
title: Resume task cleanup and CI measurements after scratch drive reconnects
kind: chore
status: closed
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4xkf4v65pthd9zbd7a5a3qv
hold: null
hold_until: null
created_at: 2026-10-14T23:05:56.308Z
updated_at: 2026-10-14T23:09:17.828Z
started_at: 2026-10-14T23:06:19.263Z
closed_at: 2026-10-14T23:09:17.827Z
close_reason: External drive reconnected and writable; CI corpus oracle resumed. Verified obsolete site-changelog preview unused via process and exact lsof checks, then staged77.8MiB allocated in external Trash; exact manifest disk-cleanup-k0rw-preview-staged.json retained. Combined task staging about902MiB, Trash unemptied; no physical-space recovery claim. Uncertain failed fixtures, historical profile and active environments preserved.
resolution: null
duplicate_of: null
---
The external scratch volume /Volumes/spud-ext1 disappeared during CI stabilization. Builds, timing pairs and external cleanup are paused under the user scratch policy. Preserve active source, external environments, private historical profile and failed-test evidence. After reconnect: verify mount/writability, recheck exact candidate handles/owners, bind generated fixture directories to retained passing receipts, stage only disposable outputs using trash with a manifest, leave Trash unemptied, then resume the fresh main602 publication oracle and paired measurements. No internal fallback.
