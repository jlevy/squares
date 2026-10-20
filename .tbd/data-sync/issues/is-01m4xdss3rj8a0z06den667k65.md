---
type: is
id: is-01m4xdss3rj8a0z06den667k65
title: Retain decimal corner tuple arity refusal in side-only presentation reader
kind: bug
status: in_progress
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4x4c32d5wdje51ep66pbzmm
hold: null
hold_until: null
created_at: 2026-10-14T14:41:57.367Z
updated_at: 2026-10-14T14:42:13.158Z
started_at: 2026-10-14T14:42:13.157Z
---
Review H2 at1c5: full decimal frame unpacks corners x,y and rejects a triple; optimized side reader indexed two literals and silently accepted a malformed third. Restore exactly-two-coordinate refusal only for decimal presentation, preserve exact materializer behavior, add direct triple-point regression for both readers.
