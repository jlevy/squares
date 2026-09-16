---
type: is
id: is-01m2nhy9nsqpwzpdgccyah2myd
title: Overlap Pages browser setup with prepared-page production
kind: bug
status: open
priority: 1
version: 1
labels:
  - ci
  - validation
dependencies: []
parent_id: is-01m2m5zjmj7dsycs1x6yxwcwwt
created_at: 2026-09-16T16:49:00.600Z
updated_at: 2026-09-16T16:49:00.600Z
---
PR #188 exact-head Pages run 35123561787 measured 235 seconds against OR-14's 180-second wall. browser-geometry (webkit) was critical: 3 seconds queued, 95 setup, 40 work, after the serialized scope+prepare chain. Start browser setup after scope and overlap it with prepare, then wait through a reusable fail-closed artifact-readiness tool before download; require an exact-head wall at or below 180 seconds.
