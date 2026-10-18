---
type: is
id: is-01m573m6xkdxqn6j7davjkmvnp
title: "PR671 review A1/A5: retain certificates without overwrite and replace manifests atomically"
kind: bug
status: in_progress
priority: 1
version: 2
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m572ssbx1x412zpvsw1sb6je
hold: null
hold_until: null
created_at: 2026-10-18T08:56:33.457Z
updated_at: 2026-10-18T09:42:48.173Z
started_at: 2026-10-18T09:42:48.172Z
---
Review https://github.com/jlevy/squares/pull/671#pullrequestreview-5562187918 at32d47d3214ec28f2a82b89689cd8bb8f63f98e02 reproduced silent overwrite/deletion of an existing plain candidate with exit0. Fix collision refusal before any write; manifest replacement must be atomic. Add fail-closed regression controls. No new expensive census is required. Preserve digest-only adapted source archive custody.
