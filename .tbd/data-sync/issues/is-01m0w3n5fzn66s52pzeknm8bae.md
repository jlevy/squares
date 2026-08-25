---
type: is
id: is-01m0w3n5fzn66s52pzeknm8bae
title: Run static gates on delegated n4 fixture test
kind: bug
status: closed
priority: 2
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - packing
  - discipline
  - testing
dependencies: []
parent_id: is-01m0tyazcycsqvm34fyxb4hdtx
created_at: 2026-08-25T09:22:38.718Z
updated_at: 2026-08-25T09:26:46.881Z
closed_at: 2026-08-25T09:26:46.880Z
close_reason: "D-262 fixed: imports and YAML boundaries repaired; Ruff passes, BasedPyright reports zero findings, and the focused fixture test passes in 0.33s."
resolution: null
duplicate_of: null
---
The delegated implementation reported complete after focused pytest only, but the maintained Ruff and BasedPyright checks exposed an unused import, unsorted imports, and six unsafe object conversions. Repair the typing/imports and require focused pytest, Ruff, and BasedPyright before closing this slice.
