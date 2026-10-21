---
type: is
id: is-01m5ft6ard4cff2y4xah2q4p2e
title: Separate primary-authored results from reported credits
kind: bug
status: closed
priority: 1
version: 5
delegate: profiles_data_integration
labels: []
dependencies: []
parent_id: is-01m5fpv2yk09g6z1a17rts4wzc
hold: null
hold_until: null
created_at: 2026-10-21T18:04:51.340Z
updated_at: 2026-10-21T20:21:47.085Z
started_at: 2026-10-21T18:04:58.450Z
closed_at: 2026-10-21T20:21:47.085Z
close_reason: Scoped profile model, identity audit and integration regressions are implemented and verified in PR 578 at 7b566ae73. Final local receipts are recorded in each bead. Exhaustive PDF coverage, historical registrations and other explicit follow-ups remain separate; overall hosted CI remains pending.
resolution: null
duplicate_of: null
---
Current result counts incorrectly include prior-work and acknowledgment credits. Derive Results only from evidenced primary authorship of the reported result; retain separate credited associations and roles. Apply to profiles, directory summaries, activity inputs and reusable project-card model as appropriate. Audit all profiles and historical/reuse cases; clarify credit count unit with user before finalizing. Astra reviews evidence rules; Sol implements shared model.

## Notes

User explicitly confirmed once per credited result. A primary-authored S5 result crediting B and C gives A one S5 Result and B/C one S5 Credit each. Primary results and non-primary credits are disjoint per person/result; deduplicate repeated mentions. Both Results and Credits have significance histograms using the crediting result score. Raw occurrence-span totals remain internal census diagnostics, not displayed Credits.

Scoped acceptance is met. Results are reviewed primary-authored result IDs; Credits are distinct nonprimary person/result associations, disjoint from that person's Results. Repeated mentions are deduplicated, significance comes from the result doing the credit, and raw occurrence spans remain diagnostics. Per-source prerequisite handling preserves the Burns/Massaccesi distinction without removing genuine coauthorship from another primary source. Project credits are received credits scoped to explicit source evidence. Original-work activity is derived independently. Shared model, profile, directory and project consumers are integrated, with meaningful synthetic and live-corpus regressions and Astra review.

Final integration receipt: commit 7b566ae73 is pushed to https://github.com/jlevy/squares/pull/578. The final rerun covered 77 previously failing cases: 76 passed in 166.02 seconds; the remaining quote-parser case was fixed and passed separately in 8.05 seconds. The coordinator reports all 68 other selected checks, the complete 121-test module run, 53 UI checks and the browser floor clean. Hosted CI remains pending under think-zpfo.
