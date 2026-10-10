---
type: is
id: is-01m4h4p5qnt2c3wmz4hkc2z01w
title: Project algebraic witness sides correctly for atlas web scaling
kind: bug
status: closed
priority: 2
version: 4
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4e35s7r1e65r1qmpz250h0p
hold: null
hold_until: null
created_at: 2026-10-09T20:11:48.843Z
updated_at: 2026-10-10T11:24:58.124Z
started_at: 2026-10-09T20:12:42.815Z
closed_at: 2026-10-10T11:24:58.124Z
close_reason: Final accepted atlas behavior implemented and published in PR474 at d83b7c03d, containing main657cc4861. Local repair-delta66PASS; hosted Fast94+actualDeferred13=107PASS on immutable mergec78974427 with identical headtree; Pages17 dependencies+required aggregatePASS; formal seniorI/correctnessJ no findings in declared scopes. Required CI PASS, no unresolvedthreads, CLEAN/MERGEABLE finalreadback. Canonical exports qualified; prior failures retained without acceptance relaxation. Later user refinements supersede earlier styling/layout requirements. Completed ready-to-merge scope; no GitHub merge performed. Browser hold, future intake and performance follow-ups remain open. Final evidence full107-final-proof.json and final-freshness.json under external final/ci-final-head-d83b7c03d.
resolution: null
duplicate_of: null
---
Main integration exposed atlas_enclosing_sides treating algebraic-number-field coefficient vectors as decimal strings. These lists encode exact scalar side lengths, not rectangular dimensions. Use the same witness parser and projection as the renderer for every selected witness scalar mode, add an algebraic-vector regression, rerun affected web/consumer checks. Keep mathematical records unchanged. Initial rectangle diagnosis corrected after inspecting witness schema.
