---
type: is
id: is-01m4cf1wk0d2f2438dac0ckz2e
title: Fix exact-form identity and retained isolator defects found by Astra
kind: task
status: in_progress
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-10-06-exact-side-values.md
delegate: codex-polynomial-01a118e4
labels: []
dependencies:
  - type: blocks
    target: is-01m4cf1w4xst7bfypgq1at86z1
parent_id: is-01m4cee7q2jdj5scgd5wa72y24
hold: null
hold_until: null
created_at: 2026-10-08T00:36:46.302Z
updated_at: 2026-10-08T01:07:33.551Z
started_at: 2026-10-08T00:37:45.020Z
---
Astra max review reproduced: builder accepts an in-cell rational approximation as exact_form for catalogue provenance because it proves only enclosure; extractor serialized centre at 60 digits while radius was 1e-109 or 1e-308, making saved interval false; extractor linear polynomial triggers log10(0). Fix all, run counterexample regressions, and have Astra re-read the resulting mathematical contracts. Feeds review think-xe25.
