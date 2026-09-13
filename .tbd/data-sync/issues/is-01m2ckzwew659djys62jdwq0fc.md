---
type: is
id: is-01m2ckzwew659djys62jdwq0fc
title: Extract one browser and Node simulation kernel with mode adapters
kind: task
status: open
priority: 1
version: 8
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels:
  - workbench-phase-3
  - workbench-roadmap
dependencies:
  - type: blocks
    target: is-01m26vyt1neawsx8w6t295mwft
  - type: blocks
    target: is-01m229am4r6vrcj7djyt78e85w
  - type: blocks
    target: is-01m229amjwvykvfz1jhnjxdap9
  - type: blocks
    target: is-01m229an1fw0az9jgk0wcbg8c4
  - type: blocks
    target: is-01m28rzfz3nnrjrqw0zdg5xvxm
parent_id: is-01m2chahf57z4w9tj5gehbs0td
created_at: 2026-09-13T05:31:39.867Z
updated_at: 2026-09-13T05:43:47.764Z
---
Implement the Phase 3 kernel and adapters exactly as specified in the governing workbench plan. Share geometry/contact/wall/broad-phase/integration code across browser and Node; separate cached Animate and live Pack state machines. Receipt includes exact poses/size/container, effective seed/config, arithmetic/timestep, work, final velocities or pose-delta residual, forcing state and termination reason. Validate the exact returned snapshot before scoring. Feasible may be transient; convergence/stationarity needs its own declared threshold/window and continuation control. Preserve independent verification. Acceptance: DOM-free import, fixed-seed pre/post parity, browser/Node receipt parity, valid/invalid/nonfinite/growth/termination controls, no copied harness physics.
