---
type: is
id: is-01m4wwt4z73vjf3nj6jsppk5jh
title: Reject encoded userinfo in changelog HTTPS targets
kind: bug
status: in_progress
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4vns6xeff13savsant84279
hold: null
hold_until: null
created_at: 2026-10-14T09:45:03.706Z
updated_at: 2026-10-14T09:45:13.325Z
started_at: 2026-10-14T09:45:13.323Z
---
Dedicated security review found encoded delimiter URLs can pass the decoded-authority no-userinfo check while emitted original URL still contains credentials. Validate original and decoded authorities, retain no-script guarantees, and add both encoded-userinfo controls before PR590 delivery.
