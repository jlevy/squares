---
type: is
id: is-01m1vrfrm0ez2wet8mq0jxa781
title: "PR #95 review PR95-R1: do not charge fixture child CPU to the test call"
kind: bug
status: in_progress
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01m1vr1dfvqt3eegay29jsnx4f
created_at: 2026-09-06T16:23:09.183Z
updated_at: 2026-09-06T16:40:41.159Z
---
Senior review https://github.com/jlevy/squares/pull/95#issuecomment-5560540217. Process child counters report reaped setup CPU during a cheap test call, making _fast_tests incorrectly require slow classification. Reproducer is /private/tmp/test_pr95_attribution_probe.py.

## Notes

Implemented in 08087a18 (final PR95 repair head 72c0df47): CPU counters are diagnostic-only, unchanged 12-second wall gate, real synchronized cross-phase child regression. Focused 115 checks and full static/record floor pass. Full reachable behavioral selection is running with the installed Cairo dylib configured; no push yet.
