---
type: is
id: is-01m229ba9mph0h3pccfvyvhbxd
title: Round out the drawn contact graph and the identity palette
kind: task
status: open
priority: 3
version: 1
spec_path: docs/project/specs/active/plan-2026-09-07-known-best-atlas-video.md
labels:
  - packing
dependencies: []
parent_id: is-01m1z68hzazv9yjs9k7cddmf82
created_at: 2026-09-09T05:13:15.828Z
updated_at: 2026-09-09T05:13:15.828Z
---
Two small gaps in the workbench prototype. The drawn contact graph has no undo, only clear-all, which makes a mis-drawn edge costly. The identity colour palette generates 42 distinguishable greens and then repeats, so at large n two squares 42 apart in identity share a colour; a second visual channel is the way out rather than more hues. Also: the rigidity slider reaches settings the fixed 1/120 s timestep cannot hold, currently reported honestly rather than clamped, which is defensible but should be decided.
