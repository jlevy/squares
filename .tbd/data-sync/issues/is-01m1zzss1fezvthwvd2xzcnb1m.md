---
type: is
id: is-01m1zzss1fezvthwvd2xzcnb1m
title: Share KPress math render readiness across native and custom hosts
kind: bug
status: in_progress
priority: 1
version: 5
labels: []
dependencies:
  - type: blocks
    target: is-01m1zzjddp742vysds0fzm3fe8
parent_id: is-01m1zzjddp742vysds0fzm3fe8
created_at: 2026-09-08T07:47:55.054Z
updated_at: 2026-09-08T08:46:24.673Z
---
Squares PR128 regex-splices six private KPress constants and duplicates runtime. Wait omits construct fonts; ResizeObserver initial delivery and early input/print/theme callbacks bypass boot readiness. Provide shared KPress API with context-correct metric selection and font readiness at actual render boundary; adopt it in squares and test delayed fonts plus dynamic updates.

## Notes

Shared KPress runtime merged in PR59 at a265d553ad2fce9f9c67a1a17b5fe8a38007e861. Every hosted check passed on c37f05c1: browser, Python3.12/3.13/3.14, lint, distribution; merge tree identical. Squares now consumes public runtime rather than copied private implementation. Final Squares integration pending.
