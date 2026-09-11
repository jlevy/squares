---
type: is
id: is-01m27m4tvdxr9kxwpjxh696x57
title: Add refusal controls for standalone threshold-verifier ceilings
kind: bug
status: closed
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m27258dy9wympsk083fspbm0
created_at: 2026-09-11T06:58:09.900Z
updated_at: 2026-09-11T07:02:39.669Z
closed_at: 2026-09-11T07:02:39.668Z
close_reason: Added one hostile-input control covering all three standalone threshold-verifier ceilings and requiring refusal before condition work. The declared-bounds gate now names each ceiling; 33 focused tests passed with two exhaustive cases deselected, Ruff passed, and BasedPyright reported zero findings.
resolution: null
duplicate_of: null
---
The T-025/T-026 standalone verifier declares maximum point-atom, threshold-atom, and direction counts. The declared-bounds gate requires each resource ceiling to be exercised by a named refusal test. Add focused mutations that exceed each ceiling, verify refusal occurs before expensive condition checks, and keep the self-contained verifier portable to CPython 3.12 or later.
