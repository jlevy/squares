---
type: is
id: is-01m2chr5bvzvbmzhsph4jcnrf9
title: Refresh PR 155 onto the current PR 125 head before cleanup validation
kind: task
status: open
priority: 1
version: 8
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels:
  - workbench-roadmap
  - workbench-phase-0
dependencies:
  - type: blocks
    target: is-01m2chahf57z4w9tj5gehbs0td
  - type: blocks
    target: is-01m2ckztpy58ydg71fkvwz7f0v
  - type: blocks
    target: is-01m2ckzvnsawqg79z9ybspc3yt
  - type: blocks
    target: is-01m2b80w08820xxzv5cfgtrhc6
  - type: blocks
    target: is-01m29f4y1r8mb8cae7ye4xv084
parent_id: is-01m28p7h39vcykq99dgjmvwv98
created_at: 2026-09-13T04:52:29.686Z
updated_at: 2026-09-13T05:45:12.341Z
---
Phase 0 integration prerequisite. At reviewed head 6e191a35, parent PR125 tip0281a508 has two missing commits: ee60689b Python spike lint/type integration and0281a508 timing artifacts; merge-base117d224f. Integrate the current parent on an isolated reviewable branch, preserve leaf seed/benchmark/results changes, and record exact parent/leaf revisions and focused baseline checks. Exit when parent changes are integrated and inherited failures are reproduced and assigned, not when downstream record repairs are complete. Passing repaired full/hosted validation belongs to think-109t and think-9sdr; requiring it here would deadlock record repair behind its own prerequisite.
