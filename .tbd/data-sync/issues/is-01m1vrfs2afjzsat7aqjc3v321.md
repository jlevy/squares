---
type: is
id: is-01m1vrfs2afjzsat7aqjc3v321
title: "PR #95 review PR95-R2: exercise a real worker in retained-source regression"
kind: bug
status: closed
priority: 2
version: 4
labels: []
dependencies: []
parent_id: is-01m1vr1dfvqt3eegay29jsnx4f
created_at: 2026-09-06T16:23:09.641Z
updated_at: 2026-09-06T16:55:23.478Z
closed_at: 2026-09-06T16:55:23.477Z
close_reason: "Addressed in PR95 head72c0df47: real two-entry spawned-worker source-path regression, mutation verified. Independent review and2303-test behavioral selection pass; pushed."
resolution: null
duplicate_of: null
---
Senior review https://github.com/jlevy/squares/pull/95#issuecomment-5560540217. Single-entry retained-source fixture clamps workers to one and never tests forkserver source-root handoff. Cover actual process execution.

## Notes

Implemented in 08087a18 (final repair head 72c0df47): two retained entries in an explicit spawn pool. Healthy regression passes; mutation ignoring supplied source_path fails with DID NOT RAISE in 2.18 seconds. Full behavioral floor pending before push.
