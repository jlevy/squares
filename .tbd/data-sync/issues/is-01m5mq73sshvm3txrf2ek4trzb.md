---
type: is
id: is-01m5mq73sshvm3txrf2ek4trzb
title: "PR #751 A6: three statements the receipts do not bear out (process count, 24 rows, timeouts)"
kind: bug
status: in_progress
priority: 3
version: 2
delegate: c-review-thmc-1023
labels: []
dependencies: []
parent_id: is-01m5mq5vh52bze2e8j4eapg0bj
hold: null
hold_until: null
created_at: 2026-10-23T15:49:03.417Z
updated_at: 2026-10-23T15:49:19.430Z
started_at: 2026-10-23T15:49:19.429Z
---
Review A, finding A6 (Low), PR #751, https://github.com/jlevy/squares/pull/751#issuecomment-6368595518. Review line 375 and the PR body (two processes; the receipt has three at once); review line 24 and evidence.yaml:43043 ('24 rows' is 24 at each of 230 and 261); review line 457 and the PR body (the timeouts 'go away' / 'remove both', though none was run and they exceed dim F 212 and dim W 11 run here).
