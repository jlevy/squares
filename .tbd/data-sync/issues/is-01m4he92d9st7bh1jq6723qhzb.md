---
type: is
id: is-01m4he92d9st7bh1jq6723qhzb
title: Fit redesigned atlas figure within the n11 paper page
kind: bug
status: closed
priority: 1
version: 3
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4h9s465x7mphy1xxkmdyqc9
hold: null
hold_until: null
created_at: 2026-10-09T22:59:25.150Z
updated_at: 2026-10-10T11:24:56.863Z
started_at: 2026-10-09T22:59:50.496Z
closed_at: 2026-10-10T11:24:56.863Z
close_reason: Final accepted atlas behavior implemented and published in PR474 at d83b7c03d, containing main657cc4861. Local repair-delta66PASS; hosted Fast94+actualDeferred13=107PASS on immutable mergec78974427 with identical headtree; Pages17 dependencies+required aggregatePASS; formal seniorI/correctnessJ no findings in declared scopes. Required CI PASS, no unresolvedthreads, CLEAN/MERGEABLE finalreadback. Canonical exports qualified; prior failures retained without acceptance relaxation. Later user refinements supersede earlier styling/layout requirements. Completed ready-to-merge scope; no GitHub merge performed. Browser hold, future intake and performance follow-ups remain open. Final evidence full107-final-proof.json and final-freshness.json under external final/ci-final-head-d83b7c03d.
resolution: null
duplicate_of: null
---
The canonical 100-packing poster is now2260x4023, but the n11 explainer print CSS forces six-inch image width with no height cap. Current production PDF has24pages with blank page6 and atlas+caption split over7-8; isolated prior Figure2 asset/dimensions control restores22pages with all current prose unchanged. Add a measured paper-only figure fit preserving full100packings, current standalone posters, caption and22-page contract; verify production font guard and page content.
