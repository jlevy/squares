---
type: is
id: is-01m2pz6fwj0rr93zap3yjqyahj
title: Show a new lower bound as a red-star 'new result' badge
kind: task
status: open
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels:
  - workbench-roadmap
dependencies: []
parent_id: is-01m28p7h39vcykq99dgjmvwv98
created_at: 2026-09-17T05:59:55.025Z
updated_at: 2026-09-17T12:07:24.749Z
---
Owner request 2026-09-17: in the facts panel, the 'new lower bound' text sits on a line of its own with uneven spacing above and below. Replace it with an icon-and-label badge, a red star with the label 'new result', built like the existing badges ('[=] exact' and the others in packages/workbench/src/view/facts.ts), shown exactly when the old line was. Done in the design-system branch (think-e50j) with a test pinning presence and absence.

## Notes

2026-09-17: PR #192 (b5ac510b), stacked on #191; fixture suppression fix 3db43561 rebased; combined-code checks pass (package 201/201, workbench pytest 311, floor contract 55, deterministic build, frontend tier). Description lists visible changes for owner review. Merge after #191.
