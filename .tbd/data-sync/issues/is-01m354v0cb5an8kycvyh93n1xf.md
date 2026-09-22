---
type: is
id: is-01m354v0cb5an8kycvyh93n1xf
title: Cross-fade the facts column so the text does not flicker between records
kind: task
status: open
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
parent_id: is-01m32t2yc3xenfb97kxn844rc7
created_at: 2026-09-22T18:07:52.202Z
updated_at: 2026-09-22T18:32:40.718Z
---
The owner (2026-09-22): 'can we make sure there's a clean transition on the text as well? It should be fast and smooth. We just don't want it to flicker because we're changing a lot of text between each record.' Every step rewrites most of the facts column at once -- the n heading, the bounds, the citation lines -- and the swap lands on one frame, which reads as a flicker at 60 fps. Give the changed text a short transition (fast, on the order of the desaturation phase, not a slow dissolve), driven off the same clock as the rest so a capture is deterministic and the cadence check still sees a clean CFR stream.

## Notes

MEASURED (2026-09-22, on the served page with citations on, step into 18, at the roll's
midpoint): layer A draws `Guzhou0806 & Mira 2026, GitHub (confirmed,` at x = 1698 and
layer B draws `This project 2026, result T-030` at the same x, both at opacity 0.5, and
the same for the upper line. The handover is already part by part -- the words `lower`
and `upper` hold at 1 and 0, the record name holds -- so nothing blinks. What the owner
sees is two DIFFERENT sentences superimposed at half ink for the middle half of the roll,
which is illegible for about 0.2 s at every step.

The area-weighted opacity is conserved across the handover (measured: monotone, no dip),
so this is not a dim beat and no brightness rule would catch it.

DESIGN. Changed parts stop crossfading through each other: the outgoing text fades out
fast and the incoming fades in a little more slowly behind it, in the shape the owner
already asked for in colour (fast out, slower in). Out over the first ~0.12 s, in over
~0.25 s, starting when the out is nearly done, so the superimposed moment is brief and at
low opacity rather than at half and half. Held parts keep swapping at the midpoint.

THE RULE THAT KEEPS IT FIXED. Extend the facts/crossfade probe's check in
check_animate_view.py: for every pair of parts whose boxes overlap and whose text
differs, min(opacity) must stay under a small bound at every sampled instant. That is
general -- it catches any future slot that superimposes two different strings -- and it is
measurable from what the probe already returns.
