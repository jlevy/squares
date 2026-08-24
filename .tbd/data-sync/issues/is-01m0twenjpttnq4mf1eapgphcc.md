---
type: is
id: is-01m0twenjpttnq4mf1eapgphcc
title: Reconcile the legacy series-000 regime boundary
kind: task
status: open
priority: 2
version: 2
spec_path: explorations/packing/campaign/series/series-000-smoke-and-calibration/README.md
labels:
  - packing
  - campaign
  - process
  - record-migration
dependencies: []
parent_id: is-01m0r7tkdt35ged6b10gaf9wa0
created_at: 2026-08-24T21:57:31.349Z
updated_at: 2026-08-24T23:02:31.252Z
---
The open legacy series-000 now contains exp-001 through exp-036 across heterogeneous search, proof, event, and exact-determination instruments. Do not perform an all-at-once migration as launch work: the explicit legacy warning plus each experiment's subject, instrument, regime, and provenance currently prevent unsafe pooling. Reopen migration when a named consumer requires series-level comparison; then identify actual comparability boundaries, open successor series only where an instrument or regime change invalidates comparison, update affected paths and series fields atomically, state carries_forward claims conservatively, regenerate views, and preserve the original S0 intent. Acceptance: the consumer's comparisons are valid, every new series has a truthful opened_because and instrument scope, no topical S1-S6 stage is mistaken for a regime boundary, and all ids, links, and generated views validate.

## Notes

2026-08-24 PR 24 review corrected the stale 35 count to exp-001 through exp-036 and downgraded eager migration. D-209 records the count error; the persisted migration remains open but is not on the launch critical path until a real series-level consumer exists.
