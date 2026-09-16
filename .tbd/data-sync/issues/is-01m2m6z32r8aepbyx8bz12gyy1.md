---
type: is
id: is-01m2m6z32r8aepbyx8bz12gyy1
title: "PR #181 review R2: strengthen converted Node test discriminators"
kind: bug
status: open
priority: 1
version: 1
labels: []
dependencies: []
parent_id: is-01m2m6xx00sabcq5zqkrneavd0
created_at: 2026-09-16T04:17:57.847Z
updated_at: 2026-09-16T04:17:57.847Z
---
Add the missing negative stand-ins named in review R2: complete zero-width image, absent squaresMath, whitespace-only text node, and throwing observer. The tests must fail on each published mutation rather than merely one sampled mutation.
