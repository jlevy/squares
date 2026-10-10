---
type: is
id: is-01m4h9vctvqc2xap8b7hb68bt0
title: "E3: close Playwright context before returning captured atlas readings"
kind: bug
status: closed
priority: 2
version: 3
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4h9s465x7mphy1xxkmdyqc9
hold: null
hold_until: null
created_at: 2026-10-09T21:42:02.815Z
updated_at: 2026-10-10T11:24:56.827Z
started_at: 2026-10-09T21:42:12.793Z
closed_at: 2026-10-10T11:24:56.827Z
close_reason: Final accepted atlas behavior implemented and published in PR474 at d83b7c03d, containing main657cc4861. Local repair-delta66PASS; hosted Fast94+actualDeferred13=107PASS on immutable mergec78974427 with identical headtree; Pages17 dependencies+required aggregatePASS; formal seniorI/correctnessJ no findings in declared scopes. Required CI PASS, no unresolvedthreads, CLEAN/MERGEABLE finalreadback. Canonical exports qualified; prior failures retained without acceptance relaxation. Later user refinements supersede earlier styling/layout requirements. Completed ready-to-merge scope; no GitHub merge performed. Browser hold, future intake and performance follow-ups remain open. Final evidence full107-final-proof.json and final-freshness.json under external final/ci-final-head-d83b7c03d.
resolution: null
duplicate_of: null
---
Independent senior review at b4b127c54 confirmed test-order fragility: the seen module fixture yields captured readings inside a live sync_playwright context and control_readings opens a second context. Geometry then centering selection reports12passed plus one setup error; isolated centering and default source order pass. Exit the existing context before returning collected readings and rerun the exact combined selection. No product-layout change.
