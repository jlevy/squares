---
type: is
id: is-01m4ygmjndn87kz50318csk62e
title: Refresh stale quick-check weights from the complete hosted cohort
kind: bug
status: in_progress
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4wtv34pphy5w434wk13b85x
hold: null
hold_until: null
created_at: 2026-10-15T00:50:47.084Z
updated_at: 2026-10-15T00:51:05.891Z
started_at: 2026-10-15T00:51:05.890Z
---
Strict cohort38658676393 at6756 has complete exit-zero pytest reports but stale scheduling weights: phase sums A788.599/B1204.565/C1666.239/D889.229, with walls232.515/336.560/450.706/243.087. Overview128.126→240.478 and site_head108.771→197.130 overload C. Refresh via existing suite_files record from all four original artifact reports, preserving source/run/attempt provenance and historical unrepresented weights, with unchanged capacities131,154,154,131. No scheduler or enforcement cap change. Collection/coverage guards and a fresh hosted cohort must verify the model; failed wrappers remain failed.
