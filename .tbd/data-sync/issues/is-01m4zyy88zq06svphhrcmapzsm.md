---
type: is
id: is-01m4zyy88zq06svphhrcmapzsm
title: Fix regularized drawing and no-script forwarding test overruns
kind: bug
status: in_progress
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: claude-code@spud10.local
labels:
  - pr-620
dependencies: []
parent_id: is-01m4wtv34pphy5w434wk13b85x
hold: null
hold_until: null
created_at: 2026-10-15T14:19:58.622Z
updated_at: 2026-10-15T14:20:22.786Z
started_at: 2026-10-15T14:20:22.786Z
---
Full checkpoint 38744311408 at cf9003e0 failed strict 12-second CALL guard on the regularized generated-block negative control (18.63 s) and no-script site-forwarder browser test (15.06 s). Preserve exact refusal and real browser navigation assertions while removing avoidable work or unnecessary waits. No cap increases, skips, or simple slow-lane relabeling. Measure scoped before/after. Root owns beads/Git/GitHub; delegated read-only diagnosis first.
