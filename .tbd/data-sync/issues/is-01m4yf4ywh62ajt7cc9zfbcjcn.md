---
type: is
id: is-01m4yf4ywh62ajt7cc9zfbcjcn
title: Reduce repeated browser reads in the project-tally filter control
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
created_at: 2026-10-15T00:24:46.736Z
updated_at: 2026-10-15T00:25:43.398Z
started_at: 2026-10-15T00:25:43.398Z
---
At6756bda8d enforced shard C reports tests/test_site_project_tallies.py::test_a_tally_link_selects_exactly_its_projects_rows at12.14s CALL against unchanged12s threshold. Diagnose actual browser/selector work and preserve every project-filter, row identity and interaction assertion. Prefer existing probe/locator batching if evidence supports it; browser code stays in typed files. No timeout raise, reduced rows, skip or narrower semantics. Original strictC job116174451226 log retained.
