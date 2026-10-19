---
type: is
id: is-01m573zdr130swtrb6r7rpv1ey
title: "PR665 review A: reconcile adoption custody, derived records, tests and publication"
kind: task
status: in_progress
priority: 1
version: 3
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m572ssbx1x412zpvsw1sb6je
hold: null
hold_until: null
created_at: 2026-10-18T09:02:40.896Z
updated_at: 2026-10-19T00:57:49.321Z
started_at: 2026-10-19T00:57:33.338Z
---
Fresh review https://github.com/jlevy/squares/pull/665#pullrequestreview-5562201404 atbb85cbb590cbd009ebe5399dd379ee4a2faeeda5: A1 High stale n236 custody attribution after38-to37 scope change; A2 High stale rigidity/chunk-derived records; A3/A4 Medium stale tests and T174335153-byte page over300000; A5 Low description.161 focused tests pass7fail. Address exact retained source and regenerate through writers; do not loosen page budget reflexively. No new certificate replay performed by this audit.

## Notes

2026-10-19 independent read-only review of local repair d6a035e30 found two Medium follow-ups before publication: (1) packing/atlas/known-best/README.md:492 states the 37 T-174 improvements range up to 4.6e-61, but exact pinned-side comparison gives max 1.7998269879545168e-19 at n308 (min 1.6965586474903646e-99 at n272); correct the upper endpoint or omit the range. (2) packing/tests/test_house_adoption.py:974 equates the 37 T-174 counts with the entire 2026-10-17 pass; #661 adds n29/T-195 on that date, so combined correct roster is 38. Make the assertion T-174-scoped and preserve both historical archive rows during integration. Review also confirmed 37 exact sides, outward rounded bounds and matching retained witnesses; custody input roster 152 matches receipt, but no fresh geometry replay. Remote #665 remains bb85cbb with failed CI; local repair is unpushed. A1-A5 dispositions, integration custody and exact-head gates still required.
