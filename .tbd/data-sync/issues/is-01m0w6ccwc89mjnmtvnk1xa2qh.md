---
type: is
id: is-01m0w6ccwc89mjnmtvnk1xa2qh
title: Promote recovered macOS deep golden from expected failure to blocking check
kind: bug
status: open
priority: 0
version: 3
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - packing
  - portability
  - gate
dependencies: []
parent_id: is-01m0vr7g27g67p699aepcdksxd
child_order_hints:
  - is-01m0w6h5t3agzyn2agwgv4zm9a
  - is-01m0w6h634tt1r8vaernzh738x
created_at: 2026-08-25T10:10:17.099Z
updated_at: 2026-08-25T10:12:53.988Z
---
PR 29 run 32835272314 proved the full focused macOS deep golden now passes, including n=4 at 4/4 converged, but the temporary D-203 expected-failure classifier deliberately turns that success into a red CI job. Remove the obsolete classifier and its tests, make the focused deep golden a direct blocking macOS step, preserve the exact pass receipt, and close only after local workflow controls and both PR jobs are green.
