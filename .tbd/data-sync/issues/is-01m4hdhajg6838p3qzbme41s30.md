---
type: is
id: is-01m4hdhajg6838p3qzbme41s30
title: Recognize retained atlas fonts as owned in PDF validation
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
created_at: 2026-10-09T22:46:27.151Z
updated_at: 2026-10-10T11:24:56.759Z
started_at: 2026-10-09T22:46:40.054Z
closed_at: 2026-10-10T11:24:56.758Z
close_reason: Final accepted atlas behavior implemented and published in PR474 at d83b7c03d, containing main657cc4861. Local repair-delta66PASS; hosted Fast94+actualDeferred13=107PASS on immutable mergec78974427 with identical headtree; Pages17 dependencies+required aggregatePASS; formal seniorI/correctnessJ no findings in declared scopes. Required CI PASS, no unresolvedthreads, CLEAN/MERGEABLE finalreadback. Canonical exports qualified; prior failures retained without acceptance relaxation. Later user refinements supersede earlier styling/layout requirements. Completed ready-to-merge scope; no GitHub merge performed. Browser hold, future intake and performance follow-ups remain open. Final evidence full107-final-proof.json and final-freshness.json under external final/ci-final-head-d83b7c03d.
resolution: null
duplicate_of: null
---
PR474 at d19d01f18 ships SquaresAtlasPrint-Bold and SquaresAtlasPrint-BoldItalic, but the production PDF font_findings checker rejects both. Register only these exact retained PostScript faces with provenance and preserve owned-font Type3, missing-embedding and unknown/lookalike refusal. Reproduce production check and browser failure; correct the font catalog/classification with narrow negative tests; qualify on macOS and hosted Linux. Root owns source integration, PR publication and final gate; no GitHub merge authorized.
