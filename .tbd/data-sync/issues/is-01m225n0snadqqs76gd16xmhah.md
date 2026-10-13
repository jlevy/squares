---
type: is
id: is-01m225n0snadqqs76gd16xmhah
title: Make the full-side contact test symmetric in the pair
kind: bug
status: open
priority: 2
version: 2
spec_path: packing/campaign/explorations/X-025-hunting-by-hand-and-the-move-set-threads.md
labels:
  - packing
dependencies: []
parent_id: is-01m225hw89vjsga1wnegrwnq5a
created_at: 2026-09-09T04:08:39.476Z
updated_at: 2026-10-13T00:55:28.485Z
---
Known defect in the v2-transitions prototype, deferred deliberately since revision 11.

The full-side contact test reads the offset between two centres in the lower-indexed square's frame rather than symmetrically, so two squares within the angle tolerance but not identical can pass one way and fail the other. Measured cost: settled on the retained frame itself, where the record should realise its own contact graph by construction, 320 of 322 frames do; n = 110 comes back 110 of 111 edges and n = 270 comes back 319 of 320, each one edge short of its own graph.

The fix is to accept the pair if either square's frame passes.

Why it was deferred, and what fixing it drags with it. The contact count is what the atlas shade rule shades by, so moving it moves the shades, and the prototype's colour checks are measured against the current build: test_candidate.py's colour sweep asserts 66 distinct fills over 20 of 20 hue families across index-all.html's 209,304 squares. Fixing the test without re-measuring those would turn a correctness fix into a wall of red. Sequence the work: fix the test, re-measure the fill census, update the checks in the same change, and say in NOTES.md which numbers moved.

Prototype: packing/atlas/known-best/video/spikes/v2-transitions/. Notes: NOTES.md, revision 11, 'The relationship graph' and 'What reads badly'.

## Notes

2026-10-13 owner decision (consolidate duplicates): think-esdm, the same defect filed under think-hsdj on 2026-09-09, closed as a duplicate of this bead. The atlas video plan's 'workbench prototype's own queue' still names think-esdm; this bead owns the fix. The defect now lives in packages/workbench/src/core/geometry.ts contactFacts, which reads the offset in the first square's frame only.
