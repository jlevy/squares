---
type: is
id: is-01m4he3z4mvvt28t2xgba2b9hw
title: Repair Linux retained atlas font alias matching
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
created_at: 2026-10-09T22:56:38.034Z
updated_at: 2026-10-10T11:24:56.775Z
started_at: 2026-10-09T22:57:05.331Z
closed_at: 2026-10-10T11:24:56.775Z
close_reason: Final accepted atlas behavior implemented and published in PR474 at d83b7c03d, containing main657cc4861. Local repair-delta66PASS; hosted Fast94+actualDeferred13=107PASS on immutable mergec78974427 with identical headtree; Pages17 dependencies+required aggregatePASS; formal seniorI/correctnessJ no findings in declared scopes. Required CI PASS, no unresolvedthreads, CLEAN/MERGEABLE finalreadback. Canonical exports qualified; prior failures retained without acceptance relaxation. Later user refinements supersede earlier styling/layout requirements. Completed ready-to-merge scope; no GitHub merge performed. Browser hold, future intake and performance follow-ups remain open. Final evidence full107-final-proof.json and final-freshness.json under external final/ci-final-head-d83b7c03d.
resolution: null
duplicate_of: null
---
Hosted Packing run 38000264420 at d19d01f18 reports 16 atlas native-font failures. Retained italic metadata family is Squares Atlas Print while Cairo receives PostScript face SquaresAtlasPrint-BoldItalic; Linux Fontconfig toy selection falls back and violates retained metrics. Add process-local exact face mapping, preserve bundled fonts and fallback refusal, and qualify on Linux. Independent private worker owns atlas_print_font.py and focused atlas/composite tests; no generated artifact change intended.
