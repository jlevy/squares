---
type: is
id: is-01m0pe76rbag3ztncnt22vvx9v
title: "Stop doing verification in one-off snippets: build the toolkit"
kind: task
status: closed
priority: 0
version: 2
spec_path: docs/project/research/research-2026-08-22-packing-11-unit-squares.md
labels: []
dependencies: []
parent_id: is-01m0pdh5bj67ca8vk7ct53g5qt
created_at: 2026-08-23T04:31:49.003Z
updated_at: 2026-08-23T04:42:03.304Z
closed_at: 2026-08-23T04:42:03.304Z
close_reason: tools/negctl.py + controls.yaml (14 controls, checked in and gated) and tools/regression_test.py (checks labelled by the defect they guard). Found D-022 on first run.
---
Diagnosis, negative controls and result analysis have been done in throwaway heredocs, repeatedly, with the same five operations rewritten each time: fetch an annealer cell, quench it, score against analytic, corrupt-a-field-and-check-the-gate-fires, summarise a JSONL by arm and cell. One of them was written wrong (a git checkout restored to HEAD and silently wiped an uncommitted backfill mid-control). Nothing was left behind for the next run. Build: (1) a negative-control harness that mutates, runs, asserts and always restores, so every control we have run becomes a permanent checked-in test; (2) a single composable CLI for anneal/quench/verify/analyze so diagnosis is repeatable and its output is archivable.
