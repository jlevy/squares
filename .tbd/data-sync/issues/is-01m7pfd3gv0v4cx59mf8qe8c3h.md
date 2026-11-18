---
type: is
id: is-01m7pfd3gv0v4cx59mf8qe8c3h
title: "PR #1028 A3 (Low): the identity count '111 to 117 beyond a thousandth' is wrong; 114 to 117"
kind: bug
status: in_progress
priority: 2
version: 2
delegate: r127b2-1118
labels: []
dependencies: []
parent_id: is-01m7pfcktsy9bnc43psx211dgs
hold: null
hold_until: null
created_at: 2026-11-18T04:42:23.643Z
updated_at: 2026-11-18T04:42:38.024Z
started_at: 2026-11-18T04:42:38.024Z
---
Severity Low. docs/project/reviews/review-2026-11-18-de-winter-1015-1017-1020-r127b.md:424. out/measure.json gives 116, 117, 117 (lower-left) and 114, 114, 114 (box-centred) under the identity; 111 is the box-centred antitranspose count at #1020. Fix: an erratum. PR #1028, review A: https://github.com/jlevy/squares/pull/1028#issuecomment-6969042368
