---
type: is
id: is-01m229ba9mph0h3pccfvyvhbxd
title: Round out the drawn contact graph and the identity palette
kind: task
status: closed
priority: 3
version: 2
spec_path: docs/project/specs/active/plan-2026-09-07-known-best-atlas-video.md
labels:
  - packing
dependencies: []
parent_id: is-01m1z68hzazv9yjs9k7cddmf82
created_at: 2026-09-09T05:13:15.828Z
updated_at: 2026-10-13T00:54:45.563Z
closed_at: 2026-10-13T00:54:45.563Z
close_reason: "Duplicate: its three parts are think-ng1e (undo, kept as the survivor), think-zt6u (identity palette) and think-7v26 (rigidity slider), filed earlier under the workbench epic."
resolution: duplicate
duplicate_of: is-01m225nvxap6cynxrpds642e8b
---
Two small gaps in the workbench prototype. The drawn contact graph has no undo, only clear-all, which makes a mis-drawn edge costly. The identity colour palette generates 42 distinguishable greens and then repeats, so at large n two squares 42 apart in identity share a colour; a second visual channel is the way out rather than more hues. Also: the rigidity slider reaches settings the fixed 1/120 s timestep cannot hold, currently reported honestly rather than clamped, which is defensible but should be decided.
