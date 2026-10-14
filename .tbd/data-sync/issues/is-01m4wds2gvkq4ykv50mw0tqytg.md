---
type: is
id: is-01m4wds2gvkq4ykv50mw0tqytg
title: Use shared glyph roles and a font-independent play icon
kind: bug
status: in_progress
priority: 1
version: 2
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4wcjctchxg9qv8jp0za5g13
hold: null
hold_until: null
created_at: 2026-10-14T05:22:19.802Z
updated_at: 2026-10-14T05:22:31.902Z
started_at: 2026-10-14T05:22:31.902Z
---
The index glyph contract reported a Grid tab at 15.2 px instead of its shared 15.7327 px role and a host-font play glyph. The implemented cleanup aligns chooser/tab labels with shared roles and draws the play icon independently of platform fonts. Relevant strong-lane validation: 5 glyph tests, 2 homepage tests and 5 Node tests passed. Keep in progress until final gate and merge. The new Regularized | Original chooser is already tracked separately as think-eq7h; this child records the existing chooser/play-button role cleanup only.
