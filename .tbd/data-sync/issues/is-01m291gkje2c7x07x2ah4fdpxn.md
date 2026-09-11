---
type: is
id: is-01m291gkje2c7x07x2ah4fdpxn
title: "Make the physics optional: a direct animation between records"
kind: feature
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-09-09-packing-strategies-as-a-shared-language.md
labels: []
dependencies: []
created_at: 2026-09-11T20:11:01.581Z
updated_at: 2026-09-11T20:11:01.581Z
---
The owner: we should be able to use this animation to avoid the physical part and simply animate between the best ones in a very direct way, or we could have the animation -- a matter of how the animation is configured in the UI.

The page already has the two halves of this. Style A ("tween") is exactly the direct animation: an interpolation from one record to the next, with the block matching so a shingled row travels as one rigid group, and no simulation at all. Styles B and C are the physics. What is missing is that the choice reads as a choice about what the film IS rather than as a choice of solver: the control is labelled by mechanism, the tween is excluded from Pack for a reason that does not apply to Animate, and nothing in the page says that one of these is a demonstration and the other is a search.

To build: name the two modes for what they produce -- a direct animation between records, and a search that has to find its way -- and let the UI say which the film is using. Then the capture receipt should record it, because "the squares moved from here to there" and "the physics found its way from here to there" are different claims and a viewer cannot tell them apart from the picture alone.

Related: the guide-phase label guard in think-zvor exists for exactly this distinction on the export side.
