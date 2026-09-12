---
type: is
id: is-01m29g1hhddhwsqfr0fz4r175e
title: "[epic] The workbench draws in layers, and one of them is the research"
kind: epic
status: open
priority: 1
version: 5
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
parent_id: is-01m28p7h39vcykq99dgjmvwv98
child_order_hints:
  - is-01m29g3y5nwwb3p5s7awrfg4vx
  - is-01m29g3z5bzj3snyzrw9pkffqp
  - is-01m29g3zzk0809kksdk904rf5w
created_at: 2026-09-12T00:24:56.608Z
updated_at: 2026-09-12T00:26:58.017Z
---
Owner's design, 2026-09-11, in three messages that are one idea:

1. "Pull in proof notes and attribution on the papers with full citation details in a clean, consistent, formatted way, just like we already have in the explainer paper in terms of styling. Optionally filled in in a way that's condensed and still fits on the page for all the pages where we have details. It would say Sources: and have the citations there, in abbreviated and concise but complete form."
2. "For ones where the lower bound is ours it should have a red star and indicate it's a new result."
3. "This should basically be a layer which is the research layer and the bounds layer, enabled/hidden as a layer in both the Pack and Animate tabs in an appropriate way."

The third is the structural one, and it turns the other two from a feature into a design. The page currently has one arrangement of facts, always on: the bar, the PROVEN block, the OPEN block, the badges. A layer model says which of those are drawn, so the same page can be a bare animation, a bounds display, or a fully cited research view -- and a capture can choose.

Three chunks:
- **think-ef9h (L1)** -- the layer model: what the layers are, how they are chosen, how the choice survives a mode switch and composes with a capture.
- **think-4kku (L2)** -- the sources layer: citations read from the record, in the explainer's own styling.
- **think-1qxd (L3)** -- the scarlet star where the lower bound is ours.

To plan in the spec before building: what the layers ARE. The obvious cut is stage / bounds / research, but "bounds" and "research" may be two depths of one layer rather than two layers, and the badges and the OPEN block have to belong somewhere.
