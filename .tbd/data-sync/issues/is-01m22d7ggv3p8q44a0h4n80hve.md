---
type: is
id: is-01m22d7ggv3p8q44a0h4n80hve
title: Refuse a container side below the area lower bound
kind: bug
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-09-07-known-best-atlas-video.md
labels:
  - packing
dependencies: []
parent_id: is-01m1z68hzazv9yjs9k7cddmf82
created_at: 2026-09-09T06:21:05.434Z
updated_at: 2026-09-09T06:21:05.434Z
---
The workbench readout will print an impossible side. With the wall repulsion set to zero the squares are free to leave the box, and an open-ended run at n = 17 then reported a required side of 4.011. Seventeen unit squares need at least sqrt(17) = 4.123 by area alone, so that number is arithmetically impossible and is a tell that the configuration is not contained rather than a good result.

The readout should refuse it: any reported side below ceil-free sqrt(n) is not a packing, whatever the pair-penetration figure says, because the penetration measure only sees square-against-square and says nothing about squares outside the walls. Report it as not contained, and say which squares are outside.

This matters beyond the degenerate setting: the whole instrument's honesty rests on never letting a sub-record number stand unqualified, and the existing guard checks overlap between squares only. Found while adding the walls' own force law, 2026-09-08.
