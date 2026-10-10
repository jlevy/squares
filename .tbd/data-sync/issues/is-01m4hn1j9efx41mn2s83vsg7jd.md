---
type: is
id: is-01m4hn1j9efx41mn2s83vsg7jd
title: Tighten shared atlas drawing gaps by a further 20 and 25 percent
kind: task
status: closed
priority: 1
version: 4
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4e35s7r1e65r1qmpz250h0p
hold: null
hold_until: null
created_at: 2026-10-10T00:57:39.372Z
updated_at: 2026-10-10T11:24:58.053Z
started_at: 2026-10-10T00:57:59.573Z
closed_at: 2026-10-10T11:24:58.053Z
close_reason: Final accepted atlas behavior implemented and published in PR474 at d83b7c03d, containing main657cc4861. Local repair-delta66PASS; hosted Fast94+actualDeferred13=107PASS on immutable mergec78974427 with identical headtree; Pages17 dependencies+required aggregatePASS; formal seniorI/correctnessJ no findings in declared scopes. Required CI PASS, no unresolvedthreads, CLEAN/MERGEABLE finalreadback. Canonical exports qualified; prior failures retained without acceptance relaxation. Later user refinements supersede earlier styling/layout requirements. Completed ready-to-merge scope; no GitHub merge performed. Browser hold, future intake and performance follow-ups remain open. Final evidence full107-final-proof.json and final-freshness.json under external final/ci-final-head-d83b7c03d.
resolution: null
duplicate_of: null
---
Apply a further 20 percent reduction to horizontal gap between actual container squares and a further 25 percent reduction to vertical gap from bottom of the case number to the next square, on web atlas overview and both PDF layouts. Preserve complete right-aligned triangle rows, grid-segment half-drawing separation, and print-only grid labels. Verify measured gap geometry and regeneration with focused checks.

## Notes

Shared print pitches203/287 retain158drawings79gridseparator; actual horizontal54.85to43.85(~20.05%) andverticalcaption78.5197to58.5197(~25.47%), sidewayslabelclearance39.465. Web adjusts actualinkgaps0.8/0.75 whilekeepingprevious drawingcapacity;12desktopreports showcomplete10/18rows and62.9/103.2/155pxdrawings. Schema/manifest/docs/paper sizeconsumers match2150x3823,4300x7646/card2150x1256,7497x5361. Focused8geometry/3consumer/3manifest-schema cases andlint/types pass. Normalfeaturef9a4f00588ab, maintainedpinb7a6c0a4e;8canonicalexports regeneration andfinalqualification pending.
