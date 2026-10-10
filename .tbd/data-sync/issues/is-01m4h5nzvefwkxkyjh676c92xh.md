---
type: is
id: is-01m4h5nzvefwkxkyjh676c92xh
title: Remove duplicate italic font preload after main integration
kind: bug
status: closed
priority: 2
version: 3
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4h26vpd0pe8frzehv70rt4p
hold: null
hold_until: null
created_at: 2026-10-09T20:29:11.404Z
updated_at: 2026-10-10T11:24:57.413Z
started_at: 2026-10-09T20:30:13.340Z
closed_at: 2026-10-10T11:24:57.413Z
close_reason: Final accepted atlas behavior implemented and published in PR474 at d83b7c03d, containing main657cc4861. Local repair-delta66PASS; hosted Fast94+actualDeferred13=107PASS on immutable mergec78974427 with identical headtree; Pages17 dependencies+required aggregatePASS; formal seniorI/correctnessJ no findings in declared scopes. Required CI PASS, no unresolvedthreads, CLEAN/MERGEABLE finalreadback. Canonical exports qualified; prior failures retained without acceptance relaxation. Later user refinements supersede earlier styling/layout requirements. Completed ready-to-merge scope; no GitHub merge performed. Browser hold, future intake and performance follow-ups remain open. Final evidence full107-final-proof.json and final-freshness.json under external final/ci-final-head-d83b7c03d.
resolution: null
duplicate_of: null
---
Independent senior review found PRELOADED_FACES lists PT Serif400italic twice after merge. Inline publication deduplicates links but direct shared head still emits duplicate hint. Remove only duplicate tuple entry, retain all four distinct regular/italic/bold/front mathfaces and focused preload-order/dedup tests. Low redundant source residue; no duplicate network fetch assertion.
