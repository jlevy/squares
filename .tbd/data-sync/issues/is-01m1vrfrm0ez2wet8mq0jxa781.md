---
type: is
id: is-01m1vrfrm0ez2wet8mq0jxa781
title: "PR #95 review PR95-R1: do not charge fixture child CPU to the test call"
kind: bug
status: closed
priority: 2
version: 4
labels: []
dependencies: []
parent_id: is-01m1vr1dfvqt3eegay29jsnx4f
created_at: 2026-09-06T16:23:09.183Z
updated_at: 2026-09-06T16:55:23.150Z
closed_at: 2026-09-06T16:55:23.149Z
close_reason: "Addressed in PR95 head72c0df47: diagnostic-only CPU with unchanged wall gate and real cross-phase regression. Independent review, static/records checks, and2303-test behavioral selection pass. Pushed to existing PR branch."
resolution: null
duplicate_of: null
---
Senior review https://github.com/jlevy/squares/pull/95#issuecomment-5560540217. Process child counters report reaped setup CPU during a cheap test call, making _fast_tests incorrectly require slow classification. Reproducer is /private/tmp/test_pr95_attribution_probe.py.

## Notes

Implemented in 08087a18 (final PR95 repair head 72c0df47): CPU counters are diagnostic-only, unchanged 12-second wall gate, real synchronized cross-phase child regression. Focused 115 checks and full static/record floor pass. Full reachable behavioral selection is running with the installed Cairo dylib configured; no push yet.
