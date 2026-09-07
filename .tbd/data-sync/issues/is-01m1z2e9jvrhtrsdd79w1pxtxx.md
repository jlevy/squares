---
type: is
id: is-01m1z2e9jvrhtrsdd79w1pxtxx
title: Reconcile the paper edits with the merged math-font integration
kind: task
status: in_progress
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m1z0patm2bp8vk8h8ntk3gwe
created_at: 2026-09-07T23:14:50.070Z
updated_at: 2026-09-07T23:15:38.466Z
---
PR114 merged into main at373beb36 while PR117 was being edited, making PR117 conflict. Preserve all requested figure/control/prose changes while merging the new kpress math-font integration, updated print-layout checks, and dependency pin. Commit reviewed local edits first, resolve conflicts with three bounded agent reviews, rebuild artifacts, and validate against the current upstream baseline before pushing.

## Notes

Reviewed paper edits saved in local commit ab3662c0 before merging main373beb36 (PR114 math-text-font integration). The standard pre-push run was intentionally interrupted at1404.87 seconds because comment-only pages.yml changes selected all slow tests; the other44 steps passed. Focused70 tests, browser/layout/touch checks, and three reviews passed. Final validation will use documented edit floor, explicit conservative relevant tests, workflow-YAML equivalence, and hosted CI; follow-up think-oe1g tracks the selector behavior.
