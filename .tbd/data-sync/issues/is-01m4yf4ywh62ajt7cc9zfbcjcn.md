---
type: is
id: is-01m4yf4ywh62ajt7cc9zfbcjcn
title: Read project-tally attribution inputs once per test invocation
kind: bug
status: in_progress
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4wtv34pphy5w434wk13b85x
hold: null
hold_until: null
created_at: 2026-10-15T00:24:46.736Z
updated_at: 2026-10-15T00:33:44.769Z
started_at: 2026-10-15T00:25:43.398Z
---
At6756bda8d strict cohort C records the exact tally-link node at12.14s CALL. Source inspection corrects the initial browser hypothesis: this is a static test with zero browser interactions. Its independent helper reads and parses the same two YAML files for each of45 project URLs:90 reads and90 parses. VE-012 preregisters a per-invocation independent attribution snapshot, complete ordered-ID equality for all45 URLs, fresh-input behavior, unchanged rendered HTML assertions and inclusive three-pair timing. Preserve all coverage and ceilings; the adjacent real browser test is unchanged.
