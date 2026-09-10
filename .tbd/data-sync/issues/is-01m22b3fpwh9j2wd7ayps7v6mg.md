---
type: is
id: is-01m22b3fpwh9j2wd7ayps7v6mg
title: Present the force law as two axes with shortcuts, not a three-state selector
kind: task
status: open
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-07-known-best-atlas-video.md
labels:
  - packing
dependencies: []
parent_id: is-01m1z68hzazv9yjs9k7cddmf82
created_at: 2026-09-09T05:43:56.379Z
updated_at: 2026-09-09T05:44:19.019Z
---
Two related presentation faults in the workbench's force law panel.

First, the rigid / soft / sticky row is drawn as a segmented control with one item highlighted, which reads as a three-state selector: the natural inference is that those are what the law IS. They are one-shot shortcuts that write into the four sliders. Nudge any slider afterwards and none of them is true any more, because a preset is an action, not a state. Draw them as buttons you press rather than a selector showing current mode, label the row as shortcuts, and make the sliders visibly move when one is pressed so it is clear what it did.

Second, the three shortcuts lie on one line but span two independent axes. Rigid to soft is one continuum, how much penetration the law tolerates before the push becomes stiff, which is entirely the repulsive branch. Stickiness is a second continuum on the attractive branch: how strongly and how far a nearly-touching pair is pulled together. A law can be rigid and sticky, or soft with no pull, and a single row cannot express those combinations. The model already splits correctly, so group the four controls under the two things they shape, the push (rigidity, repulsion strength) and the pull (attraction strength, range). If presets remain they are points in that two-dimensional space, not a line; the live curve plot is what communicates the result, since it shows both branches at once.

The measurements argue for the split. Rigid and sticky gave opposite results at different sizes: at n = 17 the rigid law was the only setting that left the trivial grid, 4.756 against sticky's 4.988, while at n = 29 it reversed, rigid jamming at 6.402 against sticky's 5.986. If the two branches do genuinely different things, the combinations are where the useful settings live. Owner's observations, 2026-09-08.
