---
type: is
id: is-01m4x4c3gx5fggqnt3ha5v8gpw
title: Use safe native YAML serialization in the complete malformed-coverage schema control
kind: bug
status: in_progress
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4wtv34pphy5w434wk13b85x
hold: null
hold_until: null
created_at: 2026-10-14T11:57:12.092Z
updated_at: 2026-10-14T11:58:08.714Z
started_at: 2026-10-14T11:58:08.714Z
---
Actual PR599 complete run38555598547 head472 malformed coverage schema-gate call12.100s/CPU lower11.40s violates unchanged12s ceiling. Retain full evidence document, malformed list field, whole validate_schemas main and exact diagnostic assertions. Replace slow safe Python serialization with semantically equal safe C emitter/fallback, prove whole-document round trip and gate refusal in measured call; no hidden setup, schema narrowing, marker or ceiling changes.
