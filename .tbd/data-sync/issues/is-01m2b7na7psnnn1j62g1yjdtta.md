---
type: is
id: is-01m2b7na7psnnn1j62g1yjdtta
title: The page can tell a packing from an overlap, and resolve one into the other
kind: feature
status: open
priority: 1
version: 9
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels:
  - workbench-roadmap
  - workbench-phase-2
dependencies:
  - type: blocks
    target: is-01m2b7nakccj4tf1tgs4k86nar
  - type: blocks
    target: is-01m2chahf57z4w9tj5gehbs0td
  - type: blocks
    target: is-01m2ckzvnsawqg79z9ybspc3yt
  - type: blocks
    target: is-01m2chr65cx0jhfd1gsmx3r31y
parent_id: is-01m28p7h39vcykq99dgjmvwv98
created_at: 2026-09-12T16:36:56.180Z
updated_at: 2026-09-13T05:43:46.788Z
---
Phase 2: expose one fail-closed count/finite/pair/wall validity contract and bounded Resolve operation shared by Pack and the headless harness. Preserve raw and repaired states, score the geometry actually displayed, report tolerance/work/termination, and validate the repaired output. Translation-only repair does not guarantee improvement, convergence or global feasibility. Resolve is an explicit action or phase, not work repeated on every paint. Acceptance: valid retained controls and invalid/nonfinite/count/wall/pair controls agree across clients; budget exhaustion is explicit; a repaired score never labels a raw frame. Historical speed and success observations are evidence to reconcile, not required outcomes.

## Notes

2026-09-12 review: preserve raw and repaired arrangements separately; compute finite pair AND wall checks with an explicit metric/tolerance, then validate repaired output. Repair is not a guarantee of best-side monotonicity or global validity. Do not compute resolution on every paint or imply the displayed raw frame has the repaired score. Introduce explicit Resolve action/phase, bounds on effort and refusal status, then same implementation for Pack/headless/Search.
