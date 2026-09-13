---
type: is
id: is-01m2e7kdn9wzf25atpz85gzdyb
title: Pack reports stationarity while the container shrinks
kind: bug
status: open
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels:
  - workbench-phase-3
  - workbench-roadmap
dependencies:
  - type: blocks
    target: is-01m2cm03rtrjcg98ejb9y56jn6
parent_id: is-01m28p7h39vcykq99dgjmvwv98
created_at: 2026-09-13T20:33:37.448Z
updated_at: 2026-09-13T20:34:39.408Z
---
The live Pack run can report a stationary state while its container schedule is still shrinking. Separate pose-motion residual from container/forcing motion and require a declared threshold/window after forcing has settled. Acceptance: a shrinking-container fixture never reports stationary; an actually settled valid control does; timeout, cancellation and completed-work receipts retain distinct termination reasons across browser and headless callers.
