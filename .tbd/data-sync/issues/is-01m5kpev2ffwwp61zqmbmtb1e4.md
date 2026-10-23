---
type: is
id: is-01m5kpev2ffwwp61zqmbmtb1e4
title: "PR #742 A3: intake_ledger.beyond_exact_sides duplicates _exact_row_side with weaker rules; recomputed does not hold an exact start to its print"
kind: bug
status: in_progress
priority: 2
version: 2
delegate: c-addr-742-1023
labels: []
dependencies: []
parent_id: is-01m5kpejtm3fmbx0sb888yj3t4
hold: null
hold_until: null
created_at: 2026-10-23T06:16:33.614Z
updated_at: 2026-10-23T06:17:00.973Z
started_at: 2026-10-23T06:17:00.973Z
---
Low, review A of PR #742 (https://github.com/jlevy/squares/pull/742#issuecomment-6358224906). packing/devtools/intake_ledger.py:1086-1112, :1270; beyond_horizon_replay.py:2514, :1885. One shared helper through read_retained_text; refuse missing or ambiguous declared records; containment check in recomputed.
