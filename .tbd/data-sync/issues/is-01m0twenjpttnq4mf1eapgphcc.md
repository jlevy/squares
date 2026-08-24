---
type: is
id: is-01m0twenjpttnq4mf1eapgphcc
title: Reconcile the legacy series-000 regime boundary
kind: task
status: open
priority: 1
version: 1
spec_path: explorations/packing/campaign/series/series-000-smoke-and-calibration/README.md
labels:
  - packing
  - campaign
  - process
  - record-migration
dependencies: []
parent_id: is-01m0r7tkdt35ged6b10gaf9wa0
created_at: 2026-08-24T21:57:31.349Z
updated_at: 2026-08-24T21:57:31.349Z
---
The open series-000 artifact still carries the original sqsearch smoke instrument and S0-only goal, while the latest record contains 35 heterogeneous search, proof, event, and exact-determination experiments. Decide and perform an all-at-once persisted-record migration: identify real comparability boundaries, open successor series only where instrumentation or regime invalidates comparison, update each affected experiment series field and path, state carries_forward claims conservatively, regenerate views, and preserve historical provenance. Do not introduce a compatibility shim or treat topical S1-S6 stages as automatic series. Acceptance: every series has a truthful opened_because and instrument scope; no experiment is compared across incompatible regimes; all ids/links/views validate; and the original S0 intent remains visible as history.
