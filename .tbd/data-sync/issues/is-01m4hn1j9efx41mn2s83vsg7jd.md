---
type: is
id: is-01m4hn1j9efx41mn2s83vsg7jd
title: Tighten shared atlas drawing gaps by a further 20 and 25 percent
kind: task
status: in_progress
priority: 1
version: 3
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4e35s7r1e65r1qmpz250h0p
hold: null
hold_until: null
created_at: 2026-10-10T00:57:39.372Z
updated_at: 2026-10-10T01:18:16.101Z
started_at: 2026-10-10T00:57:59.573Z
---
Apply a further 20 percent reduction to horizontal gap between actual container squares and a further 25 percent reduction to vertical gap from bottom of the case number to the next square, on web atlas overview and both PDF layouts. Preserve complete right-aligned triangle rows, grid-segment half-drawing separation, and print-only grid labels. Verify measured gap geometry and regeneration with focused checks.

## Notes

Shared print pitches203/287 retain158drawings79gridseparator; actual horizontal54.85to43.85(~20.05%) andverticalcaption78.5197to58.5197(~25.47%), sidewayslabelclearance39.465. Web adjusts actualinkgaps0.8/0.75 whilekeepingprevious drawingcapacity;12desktopreports showcomplete10/18rows and62.9/103.2/155pxdrawings. Schema/manifest/docs/paper sizeconsumers match2150x3823,4300x7646/card2150x1256,7497x5361. Focused8geometry/3consumer/3manifest-schema cases andlint/types pass. Normalfeaturef9a4f00588ab, maintainedpinb7a6c0a4e;8canonicalexports regeneration andfinalqualification pending.
