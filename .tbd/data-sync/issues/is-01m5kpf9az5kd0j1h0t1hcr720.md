---
type: is
id: is-01m5kpf9az5kd0j1h0t1hcr720
title: "PR #742: the #732 requests entry's n985 claim states 487b058's side, not the certificate's"
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
created_at: 2026-10-23T06:16:48.223Z
updated_at: 2026-10-23T06:17:09.872Z
started_at: 2026-10-23T06:17:09.872Z
---
Found outside review A. The certificate's exact side 151772453123382777232691846593/4754729891171500000000000000 rounds up to 31.920310216821; the entry states 31.920310217041 (487b058's side). Correct it and anything rendered from it.
