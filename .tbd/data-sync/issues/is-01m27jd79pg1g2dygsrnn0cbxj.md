---
type: is
id: is-01m27jd79pg1g2dygsrnn0cbxj
title: "A step with no slack throws the physics: overshoot the container, then shrink"
kind: bug
status: open
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-09-packing-strategies-as-a-shared-language.md
labels: []
dependencies: []
created_at: 2026-09-11T06:27:47.611Z
updated_at: 2026-09-11T06:32:19.889Z
---
The owner: adding a square to a tightly aligned row 'goes really crazy' -- the arrangement scatters violently for what should be a small change.

The suspected cause is zero slack. On a step where the record side does not grow (a prefix step, where the new square is absorbed into the existing grid), the container is the same box at n and at n + 1, and the new square has to be forced into an arrangement with no room to move. A repulsion strong enough to open a gap for it is strong enough to throw everything else.

The owner's proposal, which is also the ascent plan's Open/Close beats seen from the workbench side: grow the container PAST the target for the rearrangement, then shrink it back onto the record. A little slack is what lets the squares move past each other instead of shoving.

To do: measure first. Per step, the record side at n against n + 1 (how many steps have zero growth), and on those steps the peak displacement and peak overlap through the move. Then a container overshoot as a declared beat, with its size a parameter rather than a constant, and the same measurement after.

Related: the ascent's container mechanism in devtools/packing_strategy.py already resizes the box as a phase; this is the same idea on the page.

## Notes

MEASURED, and the owner's reading is right.

**164 of 323 steps gain no container side at all** — the box is the same at n and at n+1 — and 30 more gain under 0.02 of a side. So 194 of 323 steps (60 per cent) have no usable room. At the perfect squares the slack is exactly zero: side^2 - n is 0.000 at n = 100 and at n = 324, a full grid with no free area anywhere.

**And the new square does not travel in. It materialises at its final pose.** `renderTweenScene`/`renderPhysicsScene` draw it at `newPose` from the instant it appears, fading and scaling 0.8 -> 1.0 in place. On a step with no slack that means a unit square appearing on top of whatever currently occupies its slot, which the repulsion then has to resolve — the violence the owner sees.

Which square is 'new' is not random and not 'the middle': it is whichever target the rectangular assignment leaves over. Over the corpus: 160 steps 'prefix: square n+1 is appended', 157 'lowest cost', 5 'shared picture', 1 'lowest cost, fewest contacts, highest position'. So on a prefix step it is the record's own last square; on a matched step it can be anywhere in the final packing, interior included.

**The owner's design, to build as one beat rather than a constant:**
1. desaturate and GROW the container past the target, shown as scaling — the squares shrink relative to the box, which is what makes the room visible rather than just present;
2. bring the new square in from OUTSIDE the box rather than materialising it in the crowd;
3. let the whole set rejiggle with the slack available;
4. shrink the container back onto the record and lock in.

Open question the owner raised and worth settling with a measurement rather than a guess: where should the new square enter? Candidates — the nearest point on the container edge to its final pose; the most accessible free space; a fixed corner. It should enter with room around it either way.

Overshoot size is a parameter, not a constant. Measure peak displacement and peak overlap through the move, before and after, on the 194 no-slack steps.
