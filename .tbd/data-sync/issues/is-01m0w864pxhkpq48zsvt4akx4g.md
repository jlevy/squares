---
type: is
id: is-01m0w864pxhkpq48zsvt4akx4g
title: D-277 command text broke the defect YAML parser
kind: bug
status: open
priority: 3
version: 1
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
delegate: codex-root
labels: []
dependencies: []
parent_id: is-01m0pqg2mnmsmv8250d0rw25kb
created_at: 2026-08-25T10:41:49.276Z
updated_at: 2026-08-25T10:41:49.276Z
---
The first D-277 log entry used an unquoted backtick-leading plain scalar for regression. PyYAML rejected the entire source before defects.md could render. Convert that field to a valid folded scalar and rerun the renderer/schema gate.
