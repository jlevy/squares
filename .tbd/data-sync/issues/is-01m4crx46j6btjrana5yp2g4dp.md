---
type: is
id: is-01m4crx46j6btjrana5yp2g4dp
title: "PR #395: resolve broad push-gate regressions before completion"
kind: bug
status: open
priority: 1
version: 1
labels: []
dependencies: []
parent_id: is-01m4cecqqmt13gys8265mpra32
created_at: 2026-10-08T03:28:56.016Z
updated_at: 2026-10-08T03:28:56.016Z
---
The interrupted push gate on 1cf7ca0 passed 62 of 64 steps. Browser floor failed two design-token contracts for newly added workbench-startup CSS literals, and the broad normal Python test run showed F/E markers before interruption for the independently confirmed C3 guard correction. Diagnose with fail-fast reporting, retain meaningful contracts, fix all regressions, and rerun required push/full/exact-head hosted CI.
