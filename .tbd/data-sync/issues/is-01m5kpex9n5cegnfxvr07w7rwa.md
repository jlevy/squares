---
type: is
id: is-01m5kpex9n5cegnfxvr07w7rwa
title: "PR #742 A4: the source-history read is described more broadly than it is"
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
created_at: 2026-10-23T06:16:35.892Z
updated_at: 2026-10-23T07:42:26.594Z
started_at: 2026-10-23T06:17:03.305Z
closed_at: 2026-10-23T07:42:26.594Z
close_reason: "fixed in a1c3b0bed (comment, docstring, test) and 5d1731b43 (packet README): certificate files only; decimal poses 343-360 and the indexes measured (3285fac reported lane at 34 counts, 1.95e-16 to 7.91e-15). Reply: https://github.com/jlevy/squares/pull/742#issuecomment-6360024272"
resolution: null
duplicate_of: null
---
Low, review A of PR #742 (https://github.com/jlevy/squares/pull/742#issuecomment-6358224906). beyond_horizon_replay.py:2783-2789 (_COUNT_NAMED) and test_a_count_named_outside_the_band_is_never_read; the packet README. Say the read covers certificate files only; give the decimal poses and the indexes facts.
