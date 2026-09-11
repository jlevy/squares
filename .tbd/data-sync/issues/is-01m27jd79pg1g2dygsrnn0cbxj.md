---
type: is
id: is-01m27jd79pg1g2dygsrnn0cbxj
title: "A step with no slack throws the physics: overshoot the container, then shrink"
kind: bug
status: closed
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-09-09-packing-strategies-as-a-shared-language.md
labels: []
dependencies: []
created_at: 2026-09-11T06:27:47.611Z
updated_at: 2026-09-11T07:02:26.032Z
closed_at: 2026-09-11T07:02:26.028Z
close_reason: "Both causes fixed and measured: static appends are no longer simulated (2.46 -> 0.000 sides of thrashing at n = 324) and the container opens past its target during the move."
resolution: null
duplicate_of: null
---
The owner: adding a square to a tightly aligned row 'goes really crazy' -- the arrangement scatters violently for what should be a small change.

The suspected cause is zero slack. On a step where the record side does not grow (a prefix step, where the new square is absorbed into the existing grid), the container is the same box at n and at n + 1, and the new square has to be forced into an arrangement with no room to move. A repulsion strong enough to open a gap for it is strong enough to throw everything else.

The owner's proposal, which is also the ascent plan's Open/Close beats seen from the workbench side: grow the container PAST the target for the rearrangement, then shrink it back onto the record. A little slack is what lets the squares move past each other instead of shoving.

To do: measure first. Per step, the record side at n against n + 1 (how many steps have zero growth), and on those steps the peak displacement and peak overlap through the move. Then a container overshoot as a declared beat, with its size a parameter rather than a constant, and the same measurement after.

Related: the ascent's container mechanism in devtools/packing_strategy.py already resizes the box as a phase; this is the same idea on the page.

## Notes

Built in 14ac2ddc, and the measurement found a second cause the container could not have fixed.

FIRST CAUSE, and it was mine: a static append was being handed to the physics. The short move added in d2b2c2e7 so the new square could be seen arriving gave 160 prefix steps a simulation they never had before, with a rearrangement's worth of jiggle and no rearrangement to spend it on. Worst distance a square reached from where it ends up, in unit sides: n = 324 went 2.46, n = 100 2.26, n = 16 1.31. A static append is now drawn by the tween whatever the style says, and every one of those steps measures 0.000.

SECOND: the container now breathes. It opens PHYS.open (0.2 of a side) past the side it is heading for, is fully open by 0.3 of the move, and is closed again before the blend. The squares are not scaled; the walls move and the repulsion spreads the packing into the room on its own.

The room alone is worth little, which is the useful finding. Residual the lock-in has to carry, median over eight matched steps: baseline worst 1.171 sides / turn 23.8 deg, room only 1.117 / 22.0. It is the tightening (think-3g7w) that does the work, and the room helps it: both together at tighten 16 give 0.082 / 1.2 deg.
