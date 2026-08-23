---
type: is
id: is-01m0r8amhzzadc0enfphx0b5j1
title: "Golden: --update writes before checking oracles, and the verified pose may not be the reported side"
kind: bug
status: open
priority: 1
version: 1
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md
labels: []
dependencies: []
parent_id: is-01m0pqfp4rm5r4fy7ys6t03h0w
created_at: 2026-08-23T21:27:18.847Z
updated_at: 2026-08-23T21:27:18.847Z
---
Two confirmed defects in tools/golden_basins.py, both raised by the PR #15 review under F-16 and both re-derived from merged main.

1. WRITE-BEFORE-CHECK. main() writes the golden, THEN reports oracle failures and returns 1. A failing --update leaves an oracle-invalid golden in the worktree, which the fast path will then happily verify against itself. Fix: build, evaluate oracles, refuse to write on failure, and write atomically.

2. POSE/SIDE MISMATCH. golden_basins.py:138 keeps the FIRST pose for an identity via configs.setdefault, while sqpack/atlas.py:103 keeps the LOWEST side via basin.side = min(...). When one identity is hit twice and the second quench is better, the row reports side B while the independent verifier checked pose A. The row's `valid: true` is true of a configuration the row does not describe. Fix: verify the pose that supplies the reported side, or store the pose alongside it so the pairing is explicit.

Also from F-16 and worth doing in the same pass: SIDE_DECIMALS is 12 while the declared tier floor is 1e-11, so byte comparison can fail on differences the tier declares meaningless. Compare numeric fields at tier tolerance rather than as text.
