---
type: is
id: is-01m4wfba0syf733ywaewx49xxh
title: Restore external scratch capacity for regularization and n17 closeout gates
kind: task
status: in_progress
priority: 1
version: 2
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4w9w2vc4p0j983wvvx8pybw
hold: null
hold_until: null
created_at: 2026-10-14T05:49:45.868Z
updated_at: 2026-10-14T05:50:12.831Z
started_at: 2026-10-14T05:50:12.830Z
---
External spud-ext1 reached 100% with 32MiB free during parallel prepush/reviews. Ephemeral reviewers crashed ENOSPC; n17 prepush has temp-write infrastructure failures and regularization workers were terminated. Preserve source, Git, unique evidence and runtime history; audit concrete idle regenerable scratch outputs and restore sufficient external capacity before restarting disk-heavy gates. No fallback to internal disk.
