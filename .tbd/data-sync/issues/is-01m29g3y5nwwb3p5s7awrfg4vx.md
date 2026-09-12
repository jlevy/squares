---
type: is
id: is-01m29g3y5nwwb3p5s7awrfg4vx
title: "L1: the page draws in layers, and the choice survives a mode switch"
kind: task
status: open
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
parent_id: is-01m29g1hhddhwsqfr0fz4r175e
created_at: 2026-09-12T00:26:15.091Z
updated_at: 2026-09-12T00:26:44.563Z
---
The structural chunk, and the one to settle before either of the others is built.

The page has one arrangement of facts, always on: the gap bar, the PROVEN block, the OPEN block, the badges, the headline. A layer model says which of those are drawn.

**What the layers are is the design question**, and the obvious three-way cut may be wrong:
- *stage* -- the packing, the headline, nothing else. What a pure animation wants.
- *bounds* -- the gap bar and the two bound lines. What a viewer comparing n to n wants.
- *research* -- the sources, the attribution, the exactness and rigidity badges, the OPEN block. What a reader checking a claim wants.

The uncomfortable part is that "bounds" and "research" may be two depths of one layer rather than two layers, and the badges and the OPEN block have to belong somewhere. Work that out in the spec with the panel in front of you, not in the abstract.

**The mode interaction is the requirement that makes this more than a checkbox.** The owner asked for it "enabled/hidden as a layer in both the Pack and Animate tabs in an appropriate way" -- so a layer choice is a setting that survives a mode switch, like the style and the colour scheme do, and "appropriate" may mean the two modes have different DEFAULTS rather than different capabilities. Pack is one n examined; Animate is a sweep watched. A sweep probably wants fewer words on screen.

Constraints the existing page already imposes:
- `body.capture` already hides the controls for a capture; a layer choice has to compose with that rather than fight it.
- `setMode` is a reset as of revision 15, and a layer choice must survive it -- it belongs with `state.style`, not with the run.
- Every fact on the panel is absolutely positioned at a fixed top. Hiding one leaves a hole unless the layout reflows, so the layer model needs a layout answer, not just a `display: none`.
- The API needs `setLayers` and `layers` so a capture and the checkers can drive it.
