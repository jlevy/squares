---
type: is
id: is-01m4vbbhcsmrept7chct18jd5c
title: Re-decide the registered regularized certificates (T-154, T-155) in a validation tier
kind: task
status: open
priority: 2
version: 1
labels:
  - regularization
dependencies: []
created_at: 2026-10-13T19:20:44.693Z
updated_at: 2026-10-13T19:20:44.693Z
---
Review B5 of jlevy/squares#587 (round 1, head 05c9855dd): no gate re-decides the retained views of T-154 (59 counts, packing/cases/regularized_bounds/views/) or T-155 (n = 290, packing/cases/regularized_bounds/grid-slack-2026-10-13/views/). The tests and register_regularized_bounds --check read the committed exact-decision.json and negative-controls.json receipts; the views are not drawn, so --verify-atlas does not cover them, and no tier runs register_regularized_bounds decide or controls. The policy's question 15 (owner, 13 October 2026) says every packing, even after regularization, should be exactly verified.

Fix: a slow-lane or full-tier step that runs decide and controls for every batch into a temporary directory and compares the verdicts (not the CPU seconds) with the committed receipts. Measured cost: the grid batch decides in about 15 s and its controls take about 48 s; T-154's 59 views are larger (its receipts record the CPU seconds). OR-13 and OR-17: choose the tier by measurement and give it a wall ceiling.

Stack-wide: the gap predates the 290 layer (T-154 registered on 12 October in #549).
