---
type: is
id: is-01m4gzs7rbzw8mywvdfwfe652z
title: Add Fixed Row and Global scale controls to the web atlas
kind: feature
status: closed
priority: 2
version: 3
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4e35s7r1e65r1qmpz250h0p
hold: null
hold_until: null
created_at: 2026-10-09T18:46:06.344Z
updated_at: 2026-10-10T11:24:58.067Z
started_at: 2026-10-09T18:51:39.294Z
closed_at: 2026-10-10T11:24:58.067Z
close_reason: Final accepted atlas behavior implemented and published in PR474 at d83b7c03d, containing main657cc4861. Local repair-delta66PASS; hosted Fast94+actualDeferred13=107PASS on immutable mergec78974427 with identical headtree; Pages17 dependencies+required aggregatePASS; formal seniorI/correctnessJ no findings in declared scopes. Required CI PASS, no unresolvedthreads, CLEAN/MERGEABLE finalreadback. Canonical exports qualified; prior failures retained without acceptance relaxation. Later user refinements supersede earlier styling/layout requirements. Completed ready-to-merge scope; no GitHub merge performed. Browser hold, future intake and performance follow-ups remain open. Final evidence full107-final-proof.json and final-freshness.json under external final/ci-final-head-d83b7c03d.
resolution: null
duplicate_of: null
---
Delegate and implement a three-valued web-only Scale option: Fixed retains current same displayed container-size behavior (default); Row scales each packing relative to its logical triangular-row grid side k, so k-by-k containers have equal display size across rows and shorter enclosing sides are smaller within their row; Global scales against the largest enclosing side among cases shown by the atlas instance. Keep PDFs unchanged. Preserve Triangle/Small defaults, Grid/Medium/Large options, logical segments and half-drawing gap, count/legend semantics, uniform row slots and image/caption alignment. Use canonical actual enclosing side data, accessible controls, validated URL/default/bootstrap/no-JS behavior and meaningful rendering/unit tests; avoid unexpected layout shift. Root sole tracker/committer, source web writer disjoint from print author. Publish to current PR474 and rebuild maintained manual preview with exact current-head qualification.
