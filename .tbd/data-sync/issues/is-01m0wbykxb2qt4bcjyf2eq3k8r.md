---
type: is
id: is-01m0wbykxb2qt4bcjyf2eq3k8r
title: Exercise the early-parent-exit timeout cleanup path
kind: bug
status: closed
priority: 1
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-packing-engineering-maturity.md
delegate: codex-root
labels: []
dependencies: []
parent_id: is-01m0vpakbh6fy8p18cxsmtydgd
created_at: 2026-08-25T11:47:37.003Z
updated_at: 2026-08-25T11:57:21.123Z
closed_at: 2026-08-25T11:57:21.122Z
close_reason: "Completed before commit: the focused timeout regression now uses an output-detached SIGTERM-ignoring descendant with a delayed sentinel, and passes on macOS."
resolution: null
duplicate_of: null
---
The first uncommitted timeout regression let the descendant inherit the captured stdout pipe. That forced communicate to wait and tested only the easy TERM-then-timeout path. Replace it with a SIGTERM-ignoring child that closes or redirects output and writes a later sentinel if leaked, so the test proves the group is killed after the parent and pipe finish early.
