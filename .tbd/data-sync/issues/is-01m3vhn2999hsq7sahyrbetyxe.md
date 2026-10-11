---
type: is
id: is-01m3vhn2999hsq7sahyrbetyxe
title: Make half-angle witness exports resolve their declared schema without fallback
kind: bug
status: closed
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-10-01-post-optimality-w3-session.md
labels: []
dependencies: []
parent_id: is-01m3v9vq36ykk2jdzce75req44
created_at: 2026-10-01T10:55:06.535Z
updated_at: 2026-10-01T11:01:06.822Z
closed_at: 2026-10-01T11:01:06.809Z
close_reason: D511 export path fixed with no-fallback schema regression; 14 combined importer/parser tests pass. Raw exp235 preserved, separate portable copy validates and has exactly equal witness payload. Pushed1c90d7af4.
resolution: null
duplicate_of: null
---
Exp235 raw witness geometry passed all exact checks but importer default schema:witness.schema.yaml points beside deep output where absent. Main CLI fallback masks metadata portability defect; schema corpus omits campaign result witnesses. Preserve immutable raw run001. Fix exporter relative schema path plus no-fallback validation regression; publish separately identified schema-normalized witness with unchanged geometry and retained provenance.
