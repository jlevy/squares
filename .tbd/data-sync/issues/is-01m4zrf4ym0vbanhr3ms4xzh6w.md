---
type: is
id: is-01m4zrf4ym0vbanhr3ms4xzh6w
title: Recover completed closure scratch space while preserving source and release evidence
kind: task
status: in_progress
priority: 1
version: 3
delegate: claude-code@spud10.local
labels: []
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-15T12:26:52.243Z
updated_at: 2026-10-15T13:20:40.662Z
started_at: 2026-10-15T12:27:22.303Z
---
The external spud-ext1 volume fell to about 77 MiB free after the closure pre-push run. Hold new disk-heavy work without an internal-disk fallback. The two completed generated directories considered for recovery are tutorial-closure-20261015/tmp/pytest-of-levy/pytest-2 (about 637 MiB) and tutorial-closure-20261015/cargo-target (about 70 MiB). Producing commands have finished, and lsof/ps found no users. Source, reviewed release artifacts, raw logs and unique evidence remain in the workspace. The cleanup skill requires Trash-only staging and leaving Trash unemptied; staging on the same external volume would not free space. A direct async question requests an override for permanent removal of only these two paths. No answer has arrived, so neither has been deleted. The earlier 936 MiB staged in Trash was not physical reclamation.
