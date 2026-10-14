---
type: is
id: is-01m4wt97kj6p25mgd85yf3e89z
title: Keep unpublished infographic candidate editions stable through review corrections
kind: bug
status: in_progress
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4vns6xeff13savsant84279
hold: null
hold_until: null
created_at: 2026-10-14T09:00:52.209Z
updated_at: 2026-10-14T09:02:36.923Z
started_at: 2026-10-14T09:02:36.912Z
---
PR590 guards compare selected version with local retained output, so a correction after the first unpublished redraw wrongly demands another version bump. Compare against the authoritative published/main baseline, allow same successor version across review revisions, preserve refusal to alter an already published edition and atomic full-pair promotion, and add first-redraw/correction/rebuild controls.
