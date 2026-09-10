---
type: is
id: is-01m229b96qn93d8ykrag3jmste
title: Settle the stale mark-stroke needle in the workbench tests
kind: bug
status: open
priority: 3
version: 1
spec_path: docs/project/specs/active/plan-2026-09-07-known-best-atlas-video.md
labels:
  - packing
dependencies: []
parent_id: is-01m1z68hzazv9yjs9k7cddmf82
created_at: 2026-09-09T05:13:14.710Z
updated_at: 2026-09-09T05:13:14.710Z
---
packing/atlas/known-best/video/spikes/v2-transitions/test_candidate.py asserts a scarlet outline on the previously-arrived square, but the template sets '#mark rect { stroke: none; }' since the owner asked for no red borders. The test has failed on every run since. It is either a stale needle to flip or a real regression to restore; decide which and do it, because a permanently failing check trains everyone to ignore the suite. Note it once gated the whole browser tier off, so a stale needle here is not harmless.
