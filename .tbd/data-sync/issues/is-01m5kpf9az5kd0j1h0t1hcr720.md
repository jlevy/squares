---
type: is
id: is-01m5kpf9az5kd0j1h0t1hcr720
title: "PR #742: the #732 requests entry's n985 claim states 487b058's side, not the certificate's"
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
created_at: 2026-10-23T06:16:48.223Z
updated_at: 2026-10-23T07:42:32.468Z
started_at: 2026-10-23T06:17:09.872Z
closed_at: 2026-10-23T07:42:32.468Z
close_reason: "fixed in 24fe305ef: #732 n985 claim now 31.920310216821, the certificate's side rounded up at 12 places (was the start's 31.920310217041). Reply: https://github.com/jlevy/squares/pull/742#issuecomment-6360024272"
resolution: null
duplicate_of: null
---
Found outside review A. The certificate's exact side 151772453123382777232691846593/4754729891171500000000000000 rounds up to 31.920310216821; the entry states 31.920310217041 (487b058's side). Correct it and anything rendered from it.
