---
type: is
id: is-01m2ey0dsfhs4cfjqhy7098m7h
title: "Route D: run a real n=11 upper-bound search with exact polishing"
kind: task
status: closed
priority: 3
version: 2
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - strategy
dependencies: []
parent_id: is-01m2exznj4k1zyz1rczby8ch2k
created_at: 2026-09-14T03:05:12.238Z
updated_at: 2026-10-06T08:42:41.019Z
closed_at: 2026-10-06T08:42:41.018Z
close_reason: "Superseded: Route D searched for an n=11 packing below Trump's side and for the competing optima an optimality proof would need; T-060 proves Trump's side optimal, so both purposes are met. s(11) is settled: T-060 (V3/C3) proves s(11) = T = 3.8770835..., packing/frontier/RESULTS.md on origin/main eb43ffe9a marks every earlier n11 lower bound 'superseded by T-060', and packing/campaign/ideas.md Orientation records n11 as settled with its older route premises historical."
resolution: canceled
duplicate_of: null
---
All n=11 search so far was calibration-sized (about an hour; cold runs never found Trump's packing; every sub-Trump result was a bug). Run orientation-profile-organized search with H-017's 100x budget, basin hopping, exact polishing and rigidity checks of every endpoint <= 3.90 (including the unexplained 3.887 cluster). Low prior of a new record; the durable value is the catalogue of competing local optima an optimality proof needs. Background lane.
