---
type: is
id: is-01m5ft29c3tph6bgywc9ycwgmp
title: Fix activity years to use original work rather than later citations
kind: bug
status: closed
priority: 1
version: 4
delegate: profiles_data_integration
labels: []
dependencies: []
parent_id: is-01m5fpv2yk09g6z1a17rts4wzc
hold: null
hold_until: null
created_at: 2026-10-21T18:02:38.850Z
updated_at: 2026-10-21T20:21:47.079Z
started_at: 2026-10-21T18:02:45.713Z
closed_at: 2026-10-21T20:21:47.079Z
close_reason: Scoped profile model, identity audit and integration regressions are implemented and verified in PR 578 at 7b566ae73. Final local receipts are recorded in each bead. Exhaustive PDF coverage, historical registrations and other explicit follow-ups remain separate; overall hosted CI remains pending.
resolution: null
duplicate_of: null
---
Stromquist incorrectly displays 2026 because newer results credit his 2003 work. Systematically audit all profiles and derive years from original evidenced authored/contributed works; never later citation/reuse/import dates. Include original publications even without a dedicated registered result. Keep uncertain years blank, preserve contribution roles, add historical/multi-author/reuse regressions, and have Astra review the model.

## Notes

Scoped acceptance is met. Activity years now use reviewed original publication years, exact case finder/prover contribution years and first-party established dates. Later citations, reuse and import dates cannot extend activity. The Stromquist regression retains 2003 rather than assigning 2026 from later reuse; mixed-source publication dates, historical sources without registered results, partial dates and unknown years have focused coverage. Astra reviewed the evidence rules and live profile corpus. Undated improver activity remains explicitly unknown; the canonical dated-contribution gap is tracked by think-0ltn.

Final integration receipt: commit 7b566ae73 is pushed to https://github.com/jlevy/squares/pull/578. The final rerun covered 77 previously failing cases: 76 passed in 166.02 seconds; the remaining quote-parser case was fixed and passed separately in 8.05 seconds. The coordinator reports all 68 other selected checks, the complete 121-test module run, 53 UI checks and the browser floor clean. Hosted CI remains pending under think-zpfo.
