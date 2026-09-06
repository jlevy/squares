---
type: is
id: is-01m1t76814v4zc3za2qmnvxryy
title: Correct X-016 lower-bound rounding
kind: bug
status: closed
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m1t71acqhj675pskphwcyvst
created_at: 2026-09-06T02:01:37.048Z
updated_at: 2026-09-06T02:10:05.032Z
closed_at: 2026-09-06T02:10:05.031Z
close_reason: Corrected current strategy and audit documents to use downward-safe 3.82 and 3.85 lower-bound displays; retained full endpoints remain in the source result.
resolution: null
duplicate_of: null
---
Replace the unsafe upward-rounded ν* >= 9.907906 claim with the exact retained endpoint or a downward-safe truncation, and verify every repeated occurrence.
