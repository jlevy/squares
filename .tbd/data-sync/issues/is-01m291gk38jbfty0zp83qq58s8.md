---
type: is
id: is-01m291gk38jbfty0zp83qq58s8
title: Split the move into a rearrange phase and a correction phase
kind: feature
status: open
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
created_at: 2026-09-11T20:11:01.083Z
updated_at: 2026-09-12T01:01:31.565Z
---
The owner: the move time is really two times added together -- the physical organisation time, and then the correction time -- and they should be split out properly.

They are two different things and the beat hides it. Today one `move` covers both: the free physics rearranges, then the tightening window (PHYS.tightenFrom, 0.68 of the move) stiffens the spring, then PHYS.blend (the last 12 per cent) carries the poses onto their exact targets. A viewer sees one span; the clock offers one number; and the two halves answer different questions -- how long does the search need, against how long does the landing need.

To build: the schedule gains a third named span. `timing` becomes {dwell, rearrange, correct, settle} and the three inputs on the page become four. The tightening and the blend live inside `correct` rather than as fractions of `move`, which also makes them independent of how long the search is given -- today lengthening the move lengthens the correction with it, which is not what anyone wants.

What it buys beyond honesty: grade_motion can then price the two separately, which is the question the owner actually asks of the physics -- is it the search that is slow, or the landing.

Depends on nothing. Touches `timing`, `schedule`, `continuousTiming`, the three timing inputs, and PHYS.tightenFrom / PHYS.blend.

## Notes

IMPLEMENTED. Four phases on the page: dwell, move, correct, settle.

`move` is the free rearrangement and `correct` the landing. The two fractions that used to hide the landing inside the move -- PHYS.tightenFrom at 0.68 and PHYS.blend over the last 0.12 -- are now DERIVED from the two timings' ratio rather than fixed, so lengthening the search no longer lengthens the landing with it. The blend keeps the share of the correction it always had, three eighths.

Defaults keep today's beat exactly: 0.55 + 0.25 is the 0.8 the move was, at a ratio of 0.6875 against the 0.68 that was written down. Measured: the default duration is 2.4 s, unchanged, and each of the four controls moves it -- correct 0.25 to 1.2 takes it to 3.35, move 0.55 to 2.0 takes it to 4.8.

The correction's shape is in the trajectory cache key, because it is in the simulation: a run given more landing time is a different run, not the same one played differently.

What this now makes possible, and is the reason it was worth doing: grade_motion can price the search and the landing separately, which is the question actually being asked of the physics -- is it the search that is slow or the landing. Still to do.

Next on the same seam: think-iqvm, making the physics optional. With named phases, 'no physics' is the rearrangement being a tween.
