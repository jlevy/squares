---
type: is
id: is-01m7pfd1eeymtpqjpt6sma682h
title: "PR #1028 A2 (Low): F3 gives half the cause of E1p's failure at #1020"
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
created_at: 2026-11-18T04:42:21.518Z
updated_at: 2026-11-18T04:42:36.678Z
started_at: 2026-11-18T04:42:36.678Z
---
Severity Low. docs/project/reviews/review-2026-11-18-de-winter-1015-1017-1020-r127b.md:348-350, :567-570; packing/resources/web/de-winter-1015-1017-1020-review-r127b-2026-11-18/programs/rb127_e1p.py:4-8. Besides the top-wall squares, seven right-wall squares (51, 75, 105, 106, 121, 125, 127) lie within 1e-40 of the right wall without touching it, so the frozen rule fails at the right wall alone. Fix: an After the Freeze note correcting F3's cause; no verdict or count changes. PR #1028, review A: https://github.com/jlevy/squares/pull/1028#issuecomment-6969042368
