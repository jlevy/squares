---
type: is
id: is-01m0vp1xxetjv73j7ed841nfwz
title: Reject negative-control mutation targets outside private snapshots
kind: bug
status: closed
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m0vnq7t0x9ydha20bpdxmjzk
created_at: 2026-08-25T05:24:56.877Z
updated_at: 2026-08-25T05:37:42.309Z
closed_at: 2026-08-25T05:37:42.305Z
close_reason: Mutation targets are resolved and contained inside the private snapshot; absolute, traversal and symlink escapes are rejected and all 58 controls pass.
resolution: null
duplicate_of: null
---
devtools.run_negative_controls resolves controls.yaml file paths but does not prove the target remains inside the private snapshot. A typo, absolute path, traversal, or symlink can mutate a real checkout/external file while docs claim the harness never touches it. Add pre-read/write containment including symlink escape rejection, focused tests, defect entry, and validation.
