---
type: is
id: is-01m291gk38jbfty0zp83qq58s8
title: Split the move into a rearrange phase and a correction phase
kind: feature
status: open
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
created_at: 2026-09-11T20:11:01.083Z
updated_at: 2026-09-12T00:37:51.880Z
---
The owner: the move time is really two times added together -- the physical organisation time, and then the correction time -- and they should be split out properly.

They are two different things and the beat hides it. Today one `move` covers both: the free physics rearranges, then the tightening window (PHYS.tightenFrom, 0.68 of the move) stiffens the spring, then PHYS.blend (the last 12 per cent) carries the poses onto their exact targets. A viewer sees one span; the clock offers one number; and the two halves answer different questions -- how long does the search need, against how long does the landing need.

To build: the schedule gains a third named span. `timing` becomes {dwell, rearrange, correct, settle} and the three inputs on the page become four. The tightening and the blend live inside `correct` rather than as fractions of `move`, which also makes them independent of how long the search is given -- today lengthening the move lengthens the correction with it, which is not what anyone wants.

What it buys beyond honesty: grade_motion can then price the two separately, which is the question the owner actually asks of the physics -- is it the search that is slow, or the landing.

Depends on nothing. Touches `timing`, `schedule`, `continuousTiming`, the three timing inputs, and PHYS.tightenFrom / PHYS.blend.

## Notes

CONFIRMED NOT DONE, 2026-09-11. The owner asked again and is right: the page still offers three timings -- dwell, move, settle -- and the move still contains two phases inside it.

Their framing is the clearer one and supersedes the title: **four phases, not three.** dwell, then the physical rearrangement, then the correction, then settle. What exists today is one `move` with the correction hidden inside it as two fractions -- PHYS.tightenFrom at 0.68 of the move stiffens the spring, and PHYS.blend over the last 12 per cent carries the poses onto their exact targets -- so lengthening the move lengthens the correction with it, which is not what anyone wants and is not visible anywhere in the interface.

What to build: `timing` becomes {dwell, rearrange, correct, settle}; the three inputs on the page become four; the tightening and the blend become the whole of `correct` rather than fractions of `move`. `continuousTiming` and the beat readout follow. grade_motion can then price the search and the landing separately, which is the question actually being asked of the physics.

Also queued behind it, from the same conversation: think-iqvm, making the physics optional so a step can be animated directly between two records with no simulation at all. The two are the same seam -- if the move has named phases, 'no physics' is the rearrangement phase being the tween.
