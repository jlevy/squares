---
type: is
id: is-01m358t2tjjzw4kctvr3tec6k7
title: Refresh validation tier step counts after the PR 219 additions
kind: task
status: open
priority: 3
version: 1
labels: []
dependencies: []
created_at: 2026-09-22T19:17:16.238Z
updated_at: 2026-09-22T19:17:16.238Z
---
PR #220 related-process review: development.md Validation Loops table still labels the full gate 80 steps and records 33 of 80, while the current retained validator reports 82 total and the local records run passed 35 of 82. Refresh the current selection counts from packing-validate --list for each tier while preserving dated cost readings and topology history. The executed selection is correct; this is pre-existing explanatory-table drift from parent PR #219.
