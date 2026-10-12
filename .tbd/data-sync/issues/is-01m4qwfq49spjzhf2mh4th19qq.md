---
type: is
id: is-01m4qwfq49spjzhf2mh4th19qq
title: "Layer 6: records for the 2026-10-12 intake"
kind: task
status: in_progress
priority: 1
version: 3
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-12T11:03:09.705Z
updated_at: 2026-10-12T11:32:51.233Z
started_at: 2026-10-12T11:03:18.294Z
---
Records lane for layer 6 of stack #517 (tracker #544): merge intake-esummins, intake-watch-1012 and review-528-529 onto layer5; register T-154 (#528) and T-155 (#529), T-153 reserved for s(40) > 3359/500; adopt #528's houses on n-175, n-232, n-264; result-requests entries #521-#529 and tracking issues; intake-watch reads; render; announcement; rollups; validate.

## Notes

## Layer 6 records lane (2026-10-12), worktree agent-a52951eff0f5644d2, branch layer6

Base: layer5 at 73ae0cc89. Merges (--no-ff): intake-esummins 7d4cc96c1 (5c3d11b4d), intake-watch-1012 cfbd4e8c3 (6e4c0c9a6), review-528-529 18843516c (8c9002d9a), all clean; origin/main 0d6010ff9 (#531, #546) (3b6f2b2b9): conflicts in result-import.md (kept layer 5's answering rule, added #546's label exception), the document map (both sets), SYNOPSIS (re-rendered), release.py (layer's pin until re-pin).

Baseline packing-validate --records on the merged tree: 48/49, only the stale synopsis document map.

c70872704 register: T-154 (#528, Ostashev, 175/232/264, S3) and T-155 (#529, Calle, 102, S2, superseded by T-146 on arrival, published 2026-10-11). T-153 left reserved for s(40) > 3359/500: check_results reports "register ids are not contiguous" until it is inserted. T-149 + E-ostashev-501-certificate-report RX-4 sentence. T-152 notes, #506 entry and couzo coverage note: Couzo's 175 stays in its packet (RX-5). #521 evidence E-n011-kleddamag-3875-esummins-replay-report on T-037 (+ URL identity amendment). Bibliography: [Calle n102 2026-10-12] lineage credits-project, credit "Calle after Xu, Levy" (the plan's builds-on-project "Calle after Xu" fails test_a_sources_credit_and_lineage_agree); [Summins stratification series 2026-10-12] without lineage (no registered result cites it). No credited-names alias needed: case records credit Daniil Ostashev, already mapped.
