---
type: is
id: is-01m5kpev2ffwwp61zqmbmtb1e4
title: "PR #742 A3: intake_ledger.beyond_exact_sides duplicates _exact_row_side with weaker rules; recomputed does not hold an exact start to its print"
kind: bug
status: closed
priority: 2
version: 3
delegate: c-addr-742-1023
labels: []
dependencies: []
parent_id: is-01m5kpejtm3fmbx0sb888yj3t4
hold: null
hold_until: null
created_at: 2026-10-23T06:16:33.614Z
updated_at: 2026-10-23T07:42:24.860Z
started_at: 2026-10-23T06:17:00.973Z
closed_at: 2026-10-23T07:42:24.860Z
close_reason: "fixed in a1c3b0bed: intake_ledger.stated_exact_side is the one reader (read_retained_text; refuses missing, directory or ambiguous records), replay row_side/exact_row_side use it; recomputed holds an exact lane to its print (probe test fails before, passes after). Reply: https://github.com/jlevy/squares/pull/742#issuecomment-6360024272"
resolution: null
duplicate_of: null
---
Low, review A of PR #742 (https://github.com/jlevy/squares/pull/742#issuecomment-6358224906). packing/devtools/intake_ledger.py:1086-1112, :1270; beyond_horizon_replay.py:2514, :1885. One shared helper through read_retained_text; refuse missing or ambiguous declared records; containment check in recomputed.
