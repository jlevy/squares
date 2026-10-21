---
type: is
id: is-01m5ft6ard4cff2y4xah2q4p2e
title: Separate primary-authored results from reported credits
kind: bug
status: in_progress
priority: 1
version: 3
delegate: profiles_data_integration
labels: []
dependencies: []
parent_id: is-01m5fpv2yk09g6z1a17rts4wzc
hold: null
hold_until: null
created_at: 2026-10-21T18:04:51.340Z
updated_at: 2026-10-21T18:05:41.312Z
started_at: 2026-10-21T18:04:58.450Z
---
Current result counts incorrectly include prior-work and acknowledgment credits. Derive Results only from evidenced primary authorship of the reported result; retain separate credited associations and roles. Apply to profiles, directory summaries, activity inputs and reusable project-card model as appropriate. Audit all profiles and historical/reuse cases; clarify credit count unit with user before finalizing. Astra reviews evidence rules; Sol implements shared model.

## Notes

User explicitly confirmed once per credited result. A primary-authored S5 result crediting B and C gives A one S5 Result and B/C one S5 Credit each. Primary results and non-primary credits are disjoint per person/result; deduplicate repeated mentions. Both Results and Credits have significance histograms using the crediting result score. Raw occurrence-span totals remain internal census diagnostics, not displayed Credits.
