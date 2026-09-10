---
type: is
id: is-01m24va730rjpdgpwrbv6a8edd
title: "The atlas ascent: animate n = 1 to 100, one square at a time"
kind: task
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-09-09-packing-strategies-as-a-shared-language.md
labels: []
dependencies: []
created_at: 2026-09-10T05:05:43.007Z
updated_at: 2026-09-10T05:05:43.007Z
---
Phase 3 of the packing-strategies spec. A single directed animation from n=1 to n=100, adding one square per step and landing each time on the retained record. Directed on purpose: not a search, uses the known endpoints, clean and always arrives. Every frame comes from a guide phase and every frame is labelled guided -- the same instruments report what searches reach, and the two must never be confusable.

Five beats per step (n -> n+1): Hold the packing at rest with its label; Enter, the new square arrives from outside the container edge; Open, the container grows to the larger of the two sides; Rearrange, the guided phase drives every square to its matched target; Close, the container contracts to the new record's side.

Open and Close exist to fix a measured defect. A guided transition between two different n is smooth and lands exactly (residual 0.0004-0.0007, max per-frame motion 0.013-0.016) but squares pass through each other on the way: peak overlap 0.83 at 10->11, 0.49 at 11->12, 0.35 at 16->17, 0.86 at 17->18, roughly 100 frames of 126 carrying overlap. Between two arrangements of the SAME n the machinery is perfectly clean (peak overlap 0.0000 every frame), so it is not the mechanism -- adding a square is a genuine rearrangement with nowhere to do it.

To build: a container mechanism so the side is a phase rather than a side effect; correspondence across a change of n (the rectangular assignment already handles 100 squares against 101 targets -- it needs a rule for which square is new, and the honest one is whichever target the assignment leaves over); the ascent as one strategy document per step generated for n=1..100; capture end to end through the workbench Animate tab with a receipt naming every document and the record each step landed on; and a guard in the capture path refusing to export a guided frame without its label.

Depends on think-316d (schema and executor, now built) and think-883t (workbench plays a strategy).
