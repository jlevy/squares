---
type: is
id: is-01m1xd6geb617x4k8m7wmwj57r
title: "Phase 5: re-argue the sweeps tier ceiling from measurement and keep every fast check on the PR surface"
kind: task
status: open
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-07-atlas-expansion-to-324.md
labels: []
dependencies:
  - type: blocks
    target: is-01m1xd6grg7z892j713te59san
parent_id: is-01m1xd517vezdmp4hrmvs5c8bp
created_at: 2026-09-07T07:44:20.426Z
updated_at: 2026-09-07T07:45:04.857Z
---
Split the known-best validation step by range so each part is measured on its own; census/profile/overlay steps stay at 100 cases under D4; record measurements in gate-budgets.yaml; any step leaving the PR surface earns it by its own measured cost (OR-13). Never bump a ceiling without a measurement.
