---
type: is
id: is-01m3p45y3yxphbx0b3w5qfpyce
title: Add golden coverage for native rectangle CLI receipts
kind: task
status: closed
priority: 1
version: 3
delegate: claude-code@spud10.local
labels:
  - testing
  - golden
dependencies: []
parent_id: is-01m3nzy6gqfv60whzzvww0ffa0
hold: null
hold_until: null
created_at: 2026-09-29T08:23:27.101Z
updated_at: 2026-09-29T08:33:09.126Z
started_at: 2026-09-29T08:23:42.866Z
closed_at: 2026-09-29T08:33:09.125Z
close_reason: Added five byte-exact native rectangle CLI golden sessions with explicit update-only behavior, layered hash/mass/census/unresolved assertions, and green focused validation.
resolution: null
duplicate_of: null
---
Add small deterministic golden fixtures and regression tests for devtools.verify_rectangle_density stdout, stderr, exit status, fail-closed outcomes, and explicit update-only snapshot behavior. Layer semantic assertions over snapshots and keep normalization limited to justified unstable fields.
